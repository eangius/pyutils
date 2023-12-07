#!usr/bin/env python

# External libraries
from collections import Counter
from typing import Iterable, Tuple, List, Any, Set
from functools import cached_property, reduce

# Helper types to self document individual mappings
Node = Any
Relation = Tuple[Node, Node]


class MultiMap:
    """
    Mutable collection type that bi-directionally stores mappings
    of source & destination items. This type is similar to regular
    dictionaries except that it supports having many-to-many
    relationships in the collection. This type is also similar to
    regular tuple lists with added support for fast indexed lookup
    of items by source or destination keys. All source & destinations
    must be hashable.

    Item storage in internally handled by this class to save memory.
    Meaning any dangling source or destination nodes without
    relationships are removed from the map. While this type is memory
    based, the interface represents an abstraction between function vs
    memory mapping implementations. That is, callers need not know
    weather a mapping is derived as a computation or lookups. So all
    forward & backwards mappings of this type are possible via both
    ``[]`` indices & ``()`` calls.
    """

    def __init__(self, items: Iterable[Relation] = None):
        """
        Constructor to instantiate an new ``MultiMap``.

        Args:
            items: Optional collection of source & destination nodes to map.
        """
        self._sources = dict()  # outgoing frequencies
        self._targets = dict()  # incoming frequencies
        self._items = None      # state of iteration
        for src, dst in items or []:
            self.add(src, dst)
        return

    @cached_property
    def UNDEFINED(self):
        """
        Readonly unique symbol denoting "no-value" of node so that
        ``None`` values can be handled in mapping.
        """
        return object()

    @property
    def domain(self) -> Set[Node]:
        """
        Retrieves the current set of distinct source nodes of this map.
        """
        return set(self._sources.keys())

    @property
    def range(self) -> Set[Node]:
        """
        Retrieves the current set of distinct target nodes of this map.
        """
        return set(self._targets.keys())

    def items(self) -> Iterable[Relation]:
        """
        Retrieves the current collection of source & destination relations in this map.
        """
        return (
            (src, dst)
            for src, ctr in self._sources.items()
            for dst, freq in ctr.items()
            for _ in range(freq)
        )

    def source(self, src: Node) -> List[Node]:
        """
        Forward maps from a specific source node & returns its collection
        of related target nodes if any or empty otherwise.
        """
        return [
            dst
            for dst, freq in self._sources.get(src, dict()).items()
            for _ in range(freq)
        ]

    def target(self, dst: Node) -> List[Node]:
        """
        Backwards maps from a specific target node & returns its collection
        of related source nodes if any or empty otherwise.
        """
        return [
            src
            for src, freq in self._targets.get(dst, dict()).items()
            for _ in range(freq)
        ]

    def size(self) -> int:
        """
        Number of relationships in this map.
        """
        return sum(1 for _ in self)  # unfolded out

    def inverse(self, copy: bool = True) -> 'MultiMap':
        """
        Reverses source & destination direction mapping of all
        relationships in this map.

        Args:
            copy: To perform operation in new map or in place.

        Returns:
            result: A mapping with source & destination nodes reversed.
                Same instance whenever ``copy=False``
        """
        if copy:
            return MultiMap(
                (dst, src)
                for src, dst in self
            )
        self._sources, self._targets = self._targets, self._sources
        return self

    def add(self, src: Node, dst: Node) -> 'MultiMap':
        """
        Inplace inserts a specific relationship to this map even if
        an identical one already exists.

        Args:
            src: Source node
            dst: Destination node

        Returns:
            result: Modified instance of this map.
        """
        if src != MultiMap.UNDEFINED and dst != MultiMap.UNDEFINED:
            self._sources.setdefault(src, Counter()).update([dst])
            self._targets.setdefault(dst, Counter()).update([src])
        return self

    def remove(self, src: Node, dst: Node) -> 'MultiMap':
        """
        Inplace deletes specific relationships from this map.
        When multiple identical relationships exists, only 1 is removed.
        No effect if the relationship does not exists.

        Args:
            src: Source node. Removes all mappings from a destination when it is ``MultiMap.UNDEFINED``
            dst: Destination node. Removes all mappings from a source when it is ``MultiMap.UNDEFINED``

        Returns:
            result: Modified instance of this map.
        """
        return self.__delitem__((src, dst))

    def clear(self) -> 'MultiMap':
        """
        Inplace deletes all relationships in this map.

        Returns:
            result: Modified instance of this map.
        """
        self._sources.clear()
        self._targets.clear()
        return self

    def copy(self) -> 'MultiMap':
        """
        Creates a new but shallow clone of this mapping.
        """
        return MultiMap(self)

    # visually represent state of this map.
    def __repr__(self) -> str:
        return str(list(self))

    # number & frequency of relationships match another
    def __eq__(self, other: 'MultiMap') -> bool:
        return \
            isinstance(other, self.__class__) and \
            self._sources == other._sources and \
            self._targets == other._targets

    # union as new mapping of this & another collection
    def __add__(self, other: 'MultiMap') -> 'MultiMap':
        return reduce(
            lambda result, item: result.add(*item),
            other,
            MultiMap(self)
        )

    # difference as new mapping of this & other collection
    def __sub__(self, other: 'MultiMap') -> 'MultiMap':
        return reduce(
            lambda result, item: result.remove(*item),
            other,
            MultiMap(self)
        )

    # identify if specific source to destination mapping exists.
    def __contains__(self, item: Relation) -> bool:
        src, dst = item
        in_src = src in self._sources
        in_dst = dst in self._targets
        return \
            in_src if src != MultiMap.UNDEFINED and dst == MultiMap.UNDEFINED else \
            in_dst if src == MultiMap.UNDEFINED and dst != MultiMap.UNDEFINED else \
            in_src and in_dst

    # remove explicit relation or groups or relations.
    def __delitem__(self, item: Relation) -> 'MultiMap':
        src, dst = item

        if src != MultiMap.UNDEFINED and dst != MultiMap.UNDEFINED:
            self._decrement_frequency(self._sources, src, dst)
            self._decrement_frequency(self._targets, dst, src)
            return self

        if src != MultiMap.UNDEFINED:
            for dst in self._sources[src].keys():
                self._decrement_frequency(self._targets, dst, src)
            del self._sources[src]
            return self

        if dst != MultiMap.UNDEFINED:
            for src in self._targets[dst].keys():
                self._decrement_frequency(self._sources, src, dst)
            del self._targets[dst]
            return self

        return self.clear()

    __len__ = size          # cardinality
    __iter__ = items        # iterable like list
    __getitem__ = source    # syntactic sugar idexable like list
    __call__ = source       # syntactic sugar callable like function

    # ensure source/target keys are removed when no longer linked.
    # returns true if freq dictionary was modified.
    @staticmethod
    def _decrement_frequency(freq: dict, k, v) -> bool:
        if k not in freq:
            return False
        freq[k] -= Counter([v])
        if freq[k] == Counter():
            del freq[k]
        return True
