#!usr/bin/env python

# External libraries
from enum import Enum


#ABOUT: enhances python's default enumeration.
class Enumeration(Enum):
    @classmethod
    def items(cls) -> set:
        return set(map(lambda item: item.value, cls))

