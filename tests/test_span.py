#!usr/bin/env python

from pyutils.span import *
import pytest


@pytest.mark.unit
def test__span00():
    with pytest.raises(Exception):
        assert Span(5, 4)


@pytest.mark.unit
def test__span01():
    assert Span(0, 5).size == 6


@pytest.mark.unit
def test__span02():
    assert Span(0, 5) == Span(0, 5)
    assert Span(0, 5) != Span(6, 6)


@pytest.mark.unit
def test__span03():
    assert Span(0, 5) < Span(6, 6)
    assert Span(0, 5) <= Span(4, 9)


@pytest.mark.unit
def test__span04():
    assert Span(0, 5) > Span(-6, -3)
    assert Span(0, 5) >= Span(-2, 2)


@pytest.mark.unit
def test__span05():
    assert Span(0, 5).overlaps(Span(4, 8))
    assert not Span(0, 5).overlaps(Span(6, 8))


@pytest.mark.unit
def test__span06():
    assert Span(0, 5).adjacent(Span(5, 9))
    assert not Span(0, 5).adjacent(Span(6, 9))


@pytest.mark.unit
def test__span07():
    assert Span(0, 5).within(Span(-6, 9))
    assert not Span(0, 5).within(Span(-6, 4))


@pytest.mark.unit
def test__span08():
    assert Span(0, 5).contains(Span(2, 3))
    assert not Span(0, 5).contains(Span(2, 6))
