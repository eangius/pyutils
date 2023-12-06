#!usr/bin/env python

from python_utils.enumeration import *
import pytest


@pytest.mark.unit
def test__enumeration00():
    assert issubclass(Enumeration, Enum)
    assert Enumeration.items() == set()


@pytest.mark.unit
def test__enumeration01():
    class MyColors(str, Enumeration):
        RED = "r"
        GREEN = "g"
        BLUE = "b"
    assert MyColors.items() == {"r", "g", "b"}


@pytest.mark.unit
def test__enumeration02():
    class MyColors(int, Enumeration):
        RED = 1
        GREEN = 2
        BLUE = 3
    assert MyColors.items() == {1, 2, 3}
