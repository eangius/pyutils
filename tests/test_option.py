#!usr/bin/env python

from python_utils.option import *
import pytest


# Determine if wrapper defines something or not.
@pytest.mark.unit
def test__option01():
    assert Something(0).is_defined()
    assert not Nothing().is_defined()


# Comparisons between other entities.
@pytest.mark.unit
def test__option02():
    assert Something(0) == Something(-2 + 2)    # content equal
    assert Something(0) != Something(1)         # value diff
    assert Something(0) != Something("0")       # type diff
    assert Something(0) != Nothing()            # definition diff
    assert Nothing() == Nothing()               # undefined equals


# Factory construction
@pytest.mark.unit
def test__option03():
    assert Option(0) == Something(0)
    assert Option() == Nothing()
    assert Option() == Option()


# Gracefully fetch values if defined.
@pytest.mark.unit
def test__option04():
    assert Something(0).get() == 0
    assert not Nothing().get()


# Gracefully transform defined values as per the function.
@pytest.mark.unit
def test__option05():
    assert Nothing().map(lambda x: x + 1) == Nothing()
    assert Something(0).map(lambda x: x + 1) == Something(1)
    with pytest.raises(Exception):
        assert Something(0).map(lambda x: 1/x)
    assert Something(1).map_try(lambda x: 1) == Something(1)
    assert Something(0).map_try(lambda x: 1/x) == Nothing()
