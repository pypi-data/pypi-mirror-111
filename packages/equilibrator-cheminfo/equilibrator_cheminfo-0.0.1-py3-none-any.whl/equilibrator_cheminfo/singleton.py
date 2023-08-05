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


"""Provide a singleton metaclass."""


from __future__ import annotations

import threading


class Singleton(type):
    """Define a thread-safe singleton to be used as a metaclass."""

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        """We disallow normal class instantiation by calling the class."""
        raise RuntimeError("Please get a singleton instance via `get_instance` method.")

    def get_instance(cls, *args, **kwargs) -> Singleton:
        """Get the singleton instance of the class in a thread-safe manner."""
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
