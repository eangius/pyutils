#!usr/bin/env python

from functools import cached_property
from typing import Callable, Union


# ABOUT: enhanced dictionary data structure. This class differs from
# python's defaultdict() in that it provides cached or dynamic default
# values whenever keys are undefined without insertion side effects.
# The default values are not deemed part of the data structure & thus
# not counted towards its length.
class Dictionary(dict):
    # Since None are legit values, use a special pointer value to
    # represent undefined.
    _UNDEFINED = object()

    # Instantiate like regular dictionaries.
    def __init__(self, *args, dfl=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._static_default = dfl
        return

    @cached_property
    def default(self):
        return self._static_default

    # Dynamically accepts default values as function or scalars.
    def get(self, key, dfl: Union[Callable, object] = _UNDEFINED):
        dfl = \
            self.default if dfl == self._UNDEFINED else \
            (lambda: dfl)() if not callable(dfl) else \
            dfl()
        return super().get(key, dfl)

    # Syntactic sugar to provide static default to dict[] call.
    def __getitem__(self, key):
        return super().get(key, self.default)

    # Syntactic sugar to encapsulate fn()/dict[] implementation.
    def __call__(self, key):
        return self.get(key)
