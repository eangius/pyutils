#!usr/bin/env python
from abc import *
from typing import *


class Option(ABC):

    # Since None are legit values, use a special value pointer to
    # represent undefined.
    UNDEFINED_SENTINEL = object()

    # Factory constructor
    def __init__(self, val=UNDEFINED_SENTINEL):
        self._val = val

    # Indicates if something or nothing.
    def is_defined(self):
        return \
            isinstance(self, Something) or \
            isinstance(self, Option) and self._val != self.UNDEFINED_SENTINEL

    # Safely gets payload if available or default otherwise
    def get(self, dfl=None):
        return self._val if self.is_defined() else dfl

    # Transforms something as per the function.
    def map(self, fn: Callable = lambda x: x):
        return Something(fn(self._val)) if self.is_defined() else self

    # Attempts to transform something as per the function but
    # absorbs function failures as undefined values.
    def map_try(self, fn: Callable = lambda x: x):
        try:
            result = self.map(fn)
        except Exception:
            result = Nothing()
        return result

    # Something equals iff value & type-hierarchy equal.
    def __eq__(self, other):
        return \
            self.is_defined() == other.is_defined() and \
            self.get() == other.get()


class Nothing(Option):
    pass


class Something(Option):
    def __init__(self, val):
        super().__init__(val)
