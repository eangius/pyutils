#!usr/bin/env python

from functools import cached_property
from typing import Callable


# ABOUT: enhanced dictionary data structure. This class differs from
# pythons defaultdict() in that it provides cached or dynamic default
# values whenever keys are undefined without insertion side effects.
# The default values are not deemed part of the data structure & thus
# not counted towards its length.
class Dictionary(dict):

    # instantiate like regular dictionaries.
    def __init__(self, dfl=None, **kwargs):
        super().__init__(**kwargs)
        self._static_default = dfl
        return

    @cached_property
    def default(self):
        return self._static_default

    # Accept dynamic default values as function or scalars.
    def get(self, key, dfl=None):
        dfl = \
            self.default if dfl is None else \
            (lambda: dfl)() if not callable(dfl) else \
            dfl()
        return super().get(key, dfl)

    # Syntactic sugar to provide static default to dict[] call.
    def __getitem__(self, key):
        return super().get(key, self.default)

    # Syntactic sugar to encapsulate fn()/dict[] implementation.
    def __call__(self, key):
        return self.get(key)
