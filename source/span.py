#!usr/bin/env python
from dataclasses import dataclass
from typing import Optional


# ABOUT: immutable class like range() but supports overlap relationships,
# unbounded points.
@dataclass(frozen=True)
class Span:

    start: Optional[int] = None
    end: Optional[int] = None

    def __post_init__(self):
        if self.start and not isinstance(self.start, int):
            raise ValueError(f"Invalid span start type: {type(self.start)}")

        if self.end and not isinstance(self.end, int):
            raise ValueError(f"Invalid span end type: {type(self.end)}")

        if self.start and self.end and self.start > self.end:
            raise ValueError(f"Invalid span range: {self.start} > {self.end}")

    def items(self):
        return range(self.start, self.end + 1)

    @property
    def size(self):
        return self.end - self.start + 1

    # this string representation
    def __str__(self):
        return str(f"{self.__class__.__name__}(start={self.start}, end={self.end})")

    # equality representation
    def __hash__(self):
        return hash((self.start, self.end))

    # this exactly equal to other
    def __eq__(self, other) -> bool:
        return \
            isinstance(other, self.__class__) and \
            self.start == other.start and \
            self.end == other.end

    # this different from other
    def __ne__(self, other) -> bool:
        return \
            isinstance(other, self.__class__) and \
            self.start != other.start and \
            self.end != other.end

    # this left disjoint from other
    def __lt__(self, other) -> bool:
        return \
            isinstance(other, self.__class__) and \
            self.end < other.start

    # this right disjoint from other
    def __gt__(self, other) -> bool:
        return \
            isinstance(other, self.__class__) and \
            self.start > other.end

    # this left overlap with other
    def __le__(self, other) -> bool:
        return \
            isinstance(other, self.__class__) and \
            self.start < other.start <= self.end <= other.end

    # this right overlap with other
    def __ge__(self, other) -> bool:
        return \
            isinstance(other, self.__class__) and \
            other.start <= self.start <= other.end < self.end

    # this touching other
    def adjacent(self, other) -> bool:
        return \
            isinstance(other, self.__class__) and \
            (self.end == other.start or self.start == other.end)

    # this fully contained in other
    def within(self, other) -> bool:
        return \
            isinstance(other, self.__class__) and \
            self.start >= other.start and \
            self.end <= other.end

    # this fully encapsulates other
    def contains(self, other) -> bool:
        return \
            isinstance(other, self.__class__) and \
            self.start <= other.start and \
            self.end >= other.end

    # this overlapping other
    def overlaps(self, other) -> bool:
        return self <= other or self >= other

    # this not overlapping other
    def disjoint(self, other) -> bool:
        return not self.overlaps(other)
