#!usr/bin/env python

import pytest
from lib.span import *


def test__lib_span():
    with pytest.raises(Exception):
        assert Span(5, 4)

    assert Span(0, 5).size == 6

    assert Span(0, 5) == Span(0, 5)
    assert Span(0, 5) != Span(6, 6)

    assert Span(0, 5) < Span(6, 6)
    assert Span(0, 5) <= Span(4, 9)

    assert Span(0, 5) > Span(-6, -3)
    assert Span(0, 5) >= Span(-2, 2)

    assert Span(0, 5).overlaps(Span(4, 8))
    assert not Span(0, 5).overlaps(Span(6, 8))

    assert Span(0, 5).adjacent(Span(5, 9))
    assert not Span(0, 5).adjacent(Span(6, 9))

    assert Span(0, 5).within(Span(-6, 9))
    assert not Span(0, 5).within(Span(-6, 4))

    assert Span(0, 5).contains(Span(2, 3))
    assert not Span(0, 5).contains(Span(2, 6))
