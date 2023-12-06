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
    of pyutils & destination items. This type is similar to regular
    dictionaries except that it supports having many-to-many
    relationships in the collection. This type is also similar to
    regular tuple lists with added support for fast indexed lookup
    of items by pyutils or destination keys. All pyutils & destinations
    must be hashable.

    Item storage in internally handled by this class to save memory.
    Meaning any dangling pyutils or destination nodes without
    relationships are removed from the map. While this type is memory
    based, the interface represents an abstraction between function vs
    memory mapping implementations. That is, callers need not know
    weather a mapping is derived as a computation or lookups. So all
    forward & backwards mappings of this type are possible via both
    [] indices & () calls.
    """

    # constructor
    def __init__(self, items: Iterable[Relation] = None):
        self._sources = dict()  # outgoing frequencies
        self._targets = dict()  # incoming frequencies
        self._items = None      # state of iteration
        for src, dst in items or []:
            self.add(src, dst)
        return

    # Readonly unique symbol denoting "no-value" of node.
    # Needed so that None values can be handled in mapping.
    @cached_property
    def UNDEFINED(self):
        return object()

    @property
    def domain(self) -> Set[Node]:
        return set(self._sources.keys())

    @property
    def range(self) -> Set[Node]:
        return set(self._targets.keys())

    # current collection of relationships
    def items(self) -> Iterable[Relation]:
        return (
            (src, dst)
            for src, ctr in self._sources.items()
            for dst, freq in ctr.items()
            for _ in range(freq)
        )

    # forward map from specific pyutils or empty if no pyutils.
    def source(self, src: Node) -> List[Node]:
        return [
            dst
            for dst, freq in self._sources.get(src, dict()).items()
            for _ in range(freq)
        ]

    # backwards map from a specific target or empty if no target
    def target(self, dst: Node) -> List[Node]:
        return [
            src
            for src, freq in self._targets.get(dst, dict()).items()
            for _ in range(freq)
        ]

    # unfold & count all virtual relationships.
    def size(self) -> int:
        return sum(1 for _ in self)

    # reverses sources & destination direction either in place or with a new mapping.
    def inverse(self, copy: bool = True) -> 'MultiMap':
        if copy:
            return MultiMap(
                (dst, src)
                for src, dst in self
            )
        self._sources, self._targets = self._targets, self._sources
        return self

    # inplace inserts a specific individual mapping
    def add(self, src: Node, dst: Node) -> 'MultiMap':
        if src != MultiMap.UNDEFINED and dst != MultiMap.UNDEFINED:
            self._sources.setdefault(src, Counter()).update([dst])
            self._targets.setdefault(dst, Counter()).update([src])
        return self

    # inplace deletes a specific individual mapping if it exists.
    def remove(self, src: Node, dst: Node) -> 'MultiMap':
        return self.__delitem__((src, dst))

    # inplace clears all mappings
    def clear(self) -> 'MultiMap':
        self._sources.clear()
        self._targets.clear()
        return self

    # returns a new (shallow) copy of the mapping.
    def copy(self) -> 'MultiMap':
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

    # identify if specific pyutils to destination mapping exists.
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

    # ensure pyutils/target keys are removed when no longer linked.
    # returns true if freq dictionary was modified.
    @staticmethod
    def _decrement_frequency(freq: dict, k, v) -> bool:
        if k not in freq:
            return False
        freq[k] -= Counter([v])
        if freq[k] == Counter():
            del freq[k]
        return True
