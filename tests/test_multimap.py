#!usr/bin/env python
from python_utils.multimap import *
import pytest
import random
import string


# Maps equal itself
@pytest.mark.unit
def test__multimap_equality00(data):
    relations = MultiMap(data)
    assert relations == relations


# Maps equal content of identical self.
@pytest.mark.unit
def test__multimap_equality01(data):
    relations = MultiMap(data)
    assert relations == MultiMap(data)


# Two maps with different relationships should not equal.
@pytest.mark.unit
def test__multimap_equality02(data, random_item):
    relations = MultiMap(data)
    assert relations != MultiMap([random_item])


# Empty data should have empty source & targets
@pytest.mark.unit
def test__multimap_items00():
    relations = MultiMap()
    assert relations.domain == set()
    assert relations.range == set()


# Ensure non-duplicate sources & targets are returned.
@pytest.mark.unit
def test__multimap_items01(data):
    relations = MultiMap(data)
    assert relations.domain == {1, 2, 3, 4, None}
    assert relations.range == {'a', 'b', 'c', 'd', None}


# Empty data should have no memberships
@pytest.mark.unit
def test__multimap_membership00(data):
    assert (-1, 'z') not in MultiMap(data)


# Check for existing & non existing items.
@pytest.mark.unit
def test__multimap_membership01(data):
    relations = MultiMap(data)
    assert (1, 'a') in relations
    assert (None, 'a') in relations
    assert (1, None) in relations
    assert (1, 'z') not in relations
    assert (0, 'a') not in relations
    assert (None, 'z') not in relations
    assert (0, None) not in relations


# Retrieving data should preserve dupes.
@pytest.mark.unit
def test__multimap_iterations01(data):
    relations = MultiMap(data)
    assert list(relations) == data
    assert set(relations) == set(data)


# Arithmatic addition of relationships should yield union
@pytest.mark.unit
def test__multimap_collection01():
    m1 = MultiMap([(1, 'a'), (2, 'b')])
    m2 = MultiMap([(1, 'a')])
    result = m1 + m2
    assert id(result) != id(m1) != id(m2)
    assert result == MultiMap([(1, 'a'), (2, 'b'), (1, 'a')])
    assert len(result) == 3


# Arithmatic subtraction of relationships should yield difference
@pytest.mark.unit
def test__multimap_collection02():
    m1 = MultiMap([(1, 'a'), (2, 'b')])
    m2 = MultiMap([(1, 'a'), (1, 'a')])
    result = m1 - m2
    assert id(result) != id(m1) != id(m2)
    assert result == MultiMap([(2, 'b')])
    assert len(result) == 1


# Ensure relations are iterable (without exceptions)
@pytest.mark.unit
def test__multimap_iterable01(data):
    relations = MultiMap(data)
    assert list(relations) == list(relations.items())


# Ensure next of relationships changes.
@pytest.mark.unit
def test__mutimap_iterable02():
    relations = MultiMap([(1, 'a'), (2, 'b')])
    item = iter(relations)
    assert next(item) != next(item)


# Inverting empty yields empty
@pytest.mark.unit
def test_multimap_inverse00():
    assert MultiMap().inverse() == MultiMap()


# Inverse all relationships as a new mapping.
@pytest.mark.unit
def test__multimap_inverse01(data):
    original = MultiMap(data)
    relations = original.inverse()
    assert id(relations) != id(original)
    assert len(relations) == len(original)
    assert all(
        (src, dst) in original
        for dst, src in relations
    )
    assert relations.inverse() == original


# Inverse all relationships in place.
@pytest.mark.unit
def test__multimap_inverse02(data):
    original = MultiMap(data)
    original_items = list(original)
    relations = original.inverse(copy=False)
    assert id(relations) == id(original)
    assert len(relations) == len(original)
    assert all(
        (src, dst) in original_items
        for dst, src in relations
    )


# Epty data should have empty cardinality
@pytest.mark.unit
def test__multimap_cardinality00():
    relations = MultiMap()
    assert len(relations) == relations.size() == 0


# Count cardinality of all relationships
@pytest.mark.unit
def test__multimap_cardinality01(data):
    relations = MultiMap(data)
    assert len(relations) == relations.size() == 9


# Retrieving non existing sources should not fail
@pytest.mark.unit
def test__multimap_get00():
    relations = MultiMap()
    assert relations(0) == relations[0] == []    # non existing source


# Retrieving sources as functions or indices
@pytest.mark.unit
def test__multimap_get01(data):
    relations = MultiMap(data)
    assert relations(1) == relations[1] == ['a']
    assert relations(2) == relations[2] == ['a', 'c', 'c']
    assert relations(3) == relations[3] == ['b', 'c', 'd']
    assert relations(None) == relations[None] == ['d']
    assert relations(0) == relations[0] == []    # non existing source


# Bi-directional mapping from defined nodes should yield (possibly duplicated) relationships.
@pytest.mark.unit
def test__multimap_get02(data):
    relations = MultiMap(data)
    assert relations.source(2) == ['a', 'c', 'c']
    assert relations.target('c') == [2, 2, 3]


# Bi-directional mapping from undefined nodes should yield empty relationships
@pytest.mark.unit
def test__multimap_get04(data):
    relations = MultiMap(data)
    assert relations.source(99) == []
    assert relations.target('zz') == []


# Inserting items should add to the relationship
@pytest.mark.unit
def test__multimap_insert01(random_item):
    original = MultiMap()
    relations = original.add(*random_item)
    assert relations == MultiMap([random_item])
    assert id(relations) == id(original)


# Inserting duplicate items should add to the relation
@pytest.mark.unit
def test__multimap_insert02(random_item):
    original = MultiMap([random_item])
    relations = original.add(*random_item)
    assert relations == MultiMap([random_item]*2)
    assert id(relations) == id(original)


# Inserting illegal items should silently reject operation
@pytest.mark.unit
def test__multimap_insert03(random_item):
    src, dst = random_item
    assert MultiMap().add(src, MultiMap.UNDEFINED) == MultiMap()
    assert MultiMap().add(MultiMap.UNDEFINED, dst) == MultiMap()
    assert MultiMap().add(MultiMap.UNDEFINED, MultiMap.UNDEFINED) == MultiMap()


# Removing (possibly duplicated) specific items should drop one of the relationships
@pytest.mark.unit
def test__multimap_delete01():
    original = MultiMap([(1, "a"), (2, "c"), (2, "c")])
    relations = original.remove(2, "c")
    assert relations == MultiMap([(1, "a"), (2, "c")])
    assert id(relations) == id(original)


# Removing specific sources should drop all linked targets.
@pytest.mark.unit
def test__multimap_delete02():
    original = MultiMap([(1, "a"), (2, "a"), (2, "c")])
    relations = original.remove(2, MultiMap.UNDEFINED)
    assert relations == MultiMap([(1, "a")])
    assert id(relations) == id(original)


# Removing specific targets should drop all linked sources.
@pytest.mark.unit
def test__multimap_delete03():
    original = MultiMap([(1, "a"), (2, "a"), (2, "c")])
    relations = original.remove(MultiMap.UNDEFINED, "a")
    assert relations == MultiMap([(2, "c")])
    assert id(relations) == id(original)


# Removing all source & targets should empty the mapping.
@pytest.mark.unit
def test__multimap_delete04():
    original = MultiMap([(1, "a"), (2, "a"), (2, "c")])
    relations = original.remove(MultiMap.UNDEFINED, MultiMap.UNDEFINED)
    assert relations == MultiMap()
    assert id(relations) == id(original)


# Removing data from empty state should have no effect.
@pytest.mark.unit
def test__multimap_clear00():
    original = MultiMap()
    relations = original.clear()
    assert id(relations) == id(original)
    assert relations.domain == set()
    assert relations.range == set()
    assert relations.size() == 0


# Removing items should clear all state & return same object
@pytest.mark.unit
def test__multimap_clear01(data):
    original = MultiMap(data)
    relations = original.clear()
    assert id(relations) == id(original)
    assert relations.domain == set()
    assert relations.range == set()
    assert relations.size() == 0


# Copying a mapping should provide a shallow copy of items in a different container.
@pytest.mark.unit
def test__multimap_clone01(data):
    original = MultiMap(data)
    relations = original.copy()
    assert id(relations) != id(original)
    assert relations == original


# Sample test data with duplicate, many-to-many, mixed types & None values allowed.
@pytest.fixture
def data() -> Iterable[Relation]:
    return [
        (1, "a"), (2, "a"), (2, "c"), (2, "c"), (3, "b"), (3, "c"), (3, "d"),
        (None, 'd'), (4, None)
    ]


# Generates a random item.
@pytest.fixture
def random_item() -> Tuple[int, str]:
    src = random.randrange(0, 100)
    dst = ''.join(random.choices(string.ascii_lowercase))
    return src, dst
