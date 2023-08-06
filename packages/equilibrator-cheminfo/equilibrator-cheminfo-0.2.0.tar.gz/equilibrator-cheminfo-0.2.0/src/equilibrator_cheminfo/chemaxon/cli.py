#!/usr/bin/env python3


# Copyright (c) 2021, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provide commands for the ChemAxon Marvin pipeline."""


import argparse
import logging
import multiprocessing
import os
import sys
from pathlib import Path
from typing import Iterator, List, Optional, TypedDict

import pandas as pd
from sqlalchemy import create_engine, or_
from tqdm import tqdm

from equilibrator_cheminfo import orm
from equilibrator_cheminfo.chemaxon import (
    ChemAxonError,
    ChemAxonMolecule,
    DissociationConstant,
    MajorMicrospecies,
)
from equilibrator_cheminfo.inchi_helpers import (
    drop_column_proton_layer,
    drop_column_protonation,
)


logger = logging.getLogger()


class DissociationConstantMap(TypedDict):
    """Define an object map for a dissociation constants."""

    molecule_id: int
    value: float


class MicrospeciesMap(TypedDict):
    """Define an object map for a major microspecies."""

    molecule_id: int
    is_major: bool
    smiles: str


class ErrorMap(TypedDict):
    """Define an object map for an error message."""

    molecule_id: int
    message: str
    level: orm.SeverityLevel


class MolecularEntityMap(TypedDict, total=False):
    """Define an object map for the molecular entity."""

    id: int
    inchi_key: str
    inchi: str
    smiles: Optional[str]
    proton_dissociation_constants: Optional[List[DissociationConstantMap]]
    microspecies: Optional[List[MicrospeciesMap]]
    error_messages: Optional[List[ErrorMap]]


def extract_molecular_entities(session: orm.Session) -> pd.DataFrame:
    """Extract the molecular entities from the database into a memory bound table."""
    query = session.query(
        orm.MolecularEntity.id,
        orm.MolecularEntity.inchi_key,
        orm.MolecularEntity.inchi,
        orm.MolecularEntity.smiles,
    ).filter(
        ~orm.MolecularEntity.error_messages.any(),
        ~or_(
            orm.MolecularEntity.proton_dissociation_constants.any(),
            orm.MolecularEntity.microspecies.any(),
        ),
    )
    logger.debug("%s", query.statement)
    logger.info(f"Extract {query.count():n} molecules.")
    return pd.read_sql(query.statement, session.bind)


def _init_worker(minimum_ph: float, maximum_ph: float, fixed_ph: float) -> None:
    """Initialize a worker with globally configured ChemAxon adapters."""
    global _pka
    global _majorms

    _pka = DissociationConstant(
        minimum_ph=minimum_ph,
        minimum_basic_pka=minimum_ph,
        maximum_ph=maximum_ph,
        maximum_acidic_pka=maximum_ph,
    )
    _majorms = MajorMicrospecies(ph=fixed_ph)


def estimate_pka(
    pka: DissociationConstant, mol: ChemAxonMolecule, molecule_id: int
) -> List[DissociationConstantMap]:
    """Perform the dissociation constant prediction."""
    pka.molecule = mol
    return [
        DissociationConstantMap(molecule_id=molecule_id, value=value)
        for value in pka.get_dissociation_constants()
    ]


def estimate_majorms(
    majorms: MajorMicrospecies, mol: ChemAxonMolecule, molecule_id: int
) -> List[MicrospeciesMap]:
    """Perform the major microspecies prediction."""
    majorms.molecule = mol
    return [
        MicrospeciesMap(
            molecule_id=molecule_id,
            is_major=True,
            smiles=majorms.get_major_microspecies().get_smiles(),
        )
    ]


def create_error_maps(
    molecule_id: int, messages: List[str], severity: orm.SeverityLevel
) -> List[ErrorMap]:
    """Initialize error map objects from the given messages."""
    return [
        ErrorMap(molecule_id=molecule_id, message=msg, level=severity)
        for msg in messages
        if msg
    ]


def create_errors(molecule_id: int, error: ChemAxonError) -> List[ErrorMap]:
    """Create a list of error message from a ChemAxonError instance."""
    return create_error_maps(
        molecule_id, error.errors, orm.SeverityLevel.ERROR
    ) + create_error_maps(molecule_id, error.warnings, orm.SeverityLevel.WARNING)


def create_molecular_entity_map(molecule: MolecularEntityMap) -> MolecularEntityMap:
    """Run all ChemAxon Marvin predictions and handle errors as appropriate."""
    global _pka
    global _majorms

    try:
        if pd.notnull(molecule["smiles"]):
            mol = ChemAxonMolecule.from_smiles(molecule["smiles"])
        else:
            mol = ChemAxonMolecule.from_inchi(molecule["inchi"])
    except ChemAxonError as error:
        molecule.setdefault("error_messages", []).extend(
            create_errors(molecule["id"], error)
        )
        logger.error("Failed to create molecule from '%s'.", molecule["inchi_key"])
        return molecule

    try:
        molecule["proton_dissociation_constants"] = estimate_pka(
            _pka, mol, molecule["id"]
        )
    except RuntimeError:
        molecule.setdefault("error_messages", []).append(
            ErrorMap(
                molecule_id=molecule["id"],
                message=f"{type(_pka).__name__}: Could not reconstruct structure.",
                level=orm.SeverityLevel.ERROR,
            )
        )
    except ChemAxonError as error:
        molecule.setdefault("error_messages", []).extend(
            create_errors(molecule["id"], error)
        )

    try:
        molecule["microspecies"] = estimate_majorms(_majorms, mol, molecule["id"])
    except RuntimeError:
        molecule.setdefault("error_messages", []).append(
            ErrorMap(
                molecule_id=molecule["id"],
                message=f"{type(_majorms).__name__}: Could not reconstruct structure.",
                level=orm.SeverityLevel.ERROR,
            )
        )
    except ChemAxonError as error:
        molecule.setdefault("error_messages", []).extend(
            create_errors(molecule["id"], error)
        )

    return molecule


def record_objects(
    molecule: MolecularEntityMap,
    errors: List[ErrorMap],
    pka_values: List[DissociationConstantMap],
    microspecies: List[MicrospeciesMap],
) -> None:
    """Record molecular entity attributes in local memory."""
    errors.extend(molecule.get("error_messages", []))
    pka_values.extend(molecule.get("proton_dissociation_constants", []))
    microspecies.extend(molecule.get("microspecies", []))


def persist_objects(
    session: orm.Session,
    errors: List[ErrorMap],
    pka_values: List[DissociationConstantMap],
    microspecies: List[MicrospeciesMap],
    batch_size: int,
) -> None:
    """Persist local in-memory storage to database if the batch size is reached."""
    if len(errors) >= batch_size:
        session.bulk_insert_mappings(orm.ErrorMessage, errors)
        session.commit()
        errors.clear()
    if len(pka_values) >= batch_size:
        session.bulk_insert_mappings(orm.ProtonDissociationConstant, pka_values)
        session.commit()
        pka_values.clear()
    if len(microspecies) >= batch_size:
        session.bulk_insert_mappings(orm.Microspecies, microspecies)
        session.commit()
        microspecies.clear()


def transform_molecular_entities(
    session: orm.Session,
    molecules: pd.DataFrame,
    minimum_ph: float,
    maximum_ph: float,
    fixed_ph: float,
    processes: int,
    batch_size: int = 10_000,
) -> None:
    """Coordinate predictions on all molecules in parallel and load results."""
    args = molecules.to_dict(orient="records")
    chunk_size = min(len(args) // processes, batch_size)
    errors = []
    microspecies = []
    pka_values = []
    with multiprocessing.get_context("spawn").Pool(
        processes=processes,
        initializer=_init_worker,
        initargs=(minimum_ph, maximum_ph, fixed_ph),
    ) as pool:
        result_iter = pool.imap_unordered(
            create_molecular_entity_map,
            args,
            chunksize=chunk_size,
        )
        for mol in tqdm(result_iter, total=len(args), desc="Molecule", unit_scale=True):
            record_objects(mol, errors, pka_values, microspecies)
            persist_objects(session, errors, pka_values, microspecies, batch_size)

    persist_objects(session, errors, pka_values, microspecies, 1)


def transform_molecular_entities_sequentially(
    session: orm.Session,
    molecules: pd.DataFrame,
    minimum_ph: float,
    maximum_ph: float,
    fixed_ph: float,
    batch_size: int = 10_000,
) -> None:
    """Coordinate predictions on all molecules sequentially and load results."""
    args = (
        molecules.loc[molecules["smiles"].notnull()]
        .sample(2000)
        .to_dict(orient="records")
    )
    _init_worker(minimum_ph, maximum_ph, fixed_ph)
    errors = []
    microspecies = []
    pka_values = []
    for obj in tqdm(args, total=len(args), desc="Molecule", unit_scale=True):
        mol = create_molecular_entity_map(obj)
        record_objects(mol, errors, pka_values, microspecies)
        persist_objects(session, errors, pka_values, microspecies, batch_size)

    persist_objects(session, errors, pka_values, microspecies, 1)


def predict_microspecies(args: argparse.Namespace):
    """Coordinate high-level calls and argument transformation."""
    session = create_session(args.db_url)
    if args.processes > 1:
        transform_molecular_entities(
            session,
            extract_molecular_entities(session),
            args.minimum_ph,
            args.maximum_ph,
            args.ph,
            args.processes,
        )
    else:
        transform_molecular_entities_sequentially(
            session,
            extract_molecular_entities(session),
            args.minimum_ph,
            args.maximum_ph,
            args.ph,
        )


def create_session(db_url: str) -> orm.Session:
    """Create a SQLAlchemy session with an active database connection."""
    return orm.Session(bind=create_engine(db_url))


def extract_molecules(molecules: Path) -> pd.DataFrame:
    """Extract molecules from the given TSV file."""
    return pd.read_csv(molecules, sep="\t")


def transform_molecules(molecules: pd.DataFrame) -> pd.DataFrame:
    """Transform molecules to drop protonation information and return unique ones."""
    logger.debug("Ignore rows with missing InChIs.")
    view = molecules.loc[molecules["inchi"].notnull(), ["inchi_key", "inchi", "smiles"]]
    logger.debug("Found %d entries.", len(view))
    logger.debug("Drop protonation information.")
    result = view.copy()
    result["inchi_key"] = drop_column_protonation(result["inchi_key"])
    result["inchi"] = drop_column_proton_layer(result["inchi"])
    logger.debug("Consider unique InChIKeys only.")
    return result.drop_duplicates(["inchi_key", "inchi"])


def iter_batches(df: pd.DataFrame, batch_size: int) -> Iterator[pd.DataFrame]:
    """Return an iterator over slices of the data frame of at most batch size rows."""
    return (
        df.iloc[index : index + batch_size, :]
        for index in range(0, len(df), batch_size)
    )


def load_molecules(
    session: orm.Session, molecules: pd.DataFrame, batch_size: int = 10_000
) -> None:
    """Load the given molecules into the database."""
    with tqdm(total=len(molecules), desc="Molecule", unit_scale=True) as pbar:
        for view in iter_batches(molecules, batch_size):
            session.bulk_insert_mappings(
                orm.MolecularEntity, view.to_dict(orient="records")
            )
            session.commit()
            pbar.update(len(view))


def setup(args: argparse.Namespace) -> None:
    """Set up clean database with molecules."""
    if not args.molecules.is_file():
        raise ValueError(
            f"The TSV file '{args.molecules}' defining the molecules was not found."
        )
    session = create_session(args.db_url)
    logger.info("Set up clean database.")
    orm.Base.metadata.drop_all(session.bind)
    orm.Base.metadata.create_all(session.bind)
    logger.info("Extract molecules.")
    raw = extract_molecules(args.molecules)
    logger.info(f"Found {len(raw):n} entries.")
    logger.info("Transform molecules.")
    result = transform_molecules(raw)
    logger.info(f"Maintained {len(result):n} entries.")
    assert len(result["inchi_key"].unique()) == len(
        result
    ), "InChIKeys are not unique even though they *should* be."
    logger.info("Load molecules.")
    load_molecules(session, result)
    logger.info("Done.")


def parse_argv() -> argparse.Namespace:
    """Define the command line arguments and immediately parse them."""
    num_processes = len(os.sched_getaffinity(0))
    if not num_processes:
        num_processes = 1
    if num_processes > 1:
        num_processes -= 1

    parser = argparse.ArgumentParser(
        prog="marvin.py",
        description="Build a molecular entity database containing dissociation "
        "constants and major microspecies using ChemAxon.",
    )
    parser.add_argument(
        "--db-url",
        required=True,
        metavar="URL",
        help="A string interpreted as an rfc1738 compatible database URL.",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        default="INFO",
        help="The desired log level.",
        choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
    )
    sub_parsers = parser.add_subparsers()

    setup_parser = sub_parsers.add_parser("setup")
    setup_parser.add_argument(
        "molecules",
        type=Path,
        help="Path to a TSV file with molecules defined by the columns inchi_key, "
        "inchi, smiles. Missing values are allowed.",
    )
    setup_parser.set_defaults(func=setup)

    microspecies_parser = sub_parsers.add_parser("microspecies")
    microspecies_parser.add_argument(
        "--minimum-ph",
        type=float,
        default=0.0,
        help="The minimum pH value to consider (default 0).",
    )
    microspecies_parser.add_argument(
        "--maximum-ph",
        type=float,
        default=14.0,
        help="The maximum pH value to consider (default 14).",
    )
    microspecies_parser.add_argument(
        "--ph",
        type=float,
        default=7.0,
        help="The pH value at which to determine the major microspecies (default 7).",
    )
    microspecies_parser.add_argument(
        "--processes",
        type=int,
        default=num_processes,
        help=f"The number of parallel processes to start (default {num_processes}).",
    )
    microspecies_parser.set_defaults(func=predict_microspecies)

    return parser.parse_args(sys.argv[1:])


def main() -> None:
    """Coordinate argument parsing and command calling."""
    args = parse_argv()
    logging.basicConfig(level=args.log_level, format="[%(levelname)s] %(message)s")
    args.func(args)
