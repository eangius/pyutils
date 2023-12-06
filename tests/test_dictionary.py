#!usr/bin/env python

from python_utils.dictionary import *
import pytest
import datetime


@pytest.mark.unit
def test__dictionary00():
    assert isinstance(Dictionary(), dict)


@pytest.mark.unit
def test__dictionary01():
    assert Dictionary() == {}


@pytest.mark.unit
def test__dictionary02(regular_dict):
    assert Dictionary(regular_dict) == regular_dict


@pytest.mark.unit
def test__dictionary03(regular_dict):
    assert Dictionary(key1="value", key2=2) == regular_dict


@pytest.mark.unit
def test__dictionary04(regular_dict):
    assert Dictionary(regular_dict, dfl=datetime.datetime.now()) == regular_dict


@pytest.mark.unit
def test__dictionary05(regular_dict):
    assert Dictionary(dfl=datetime.datetime.now()) == {}  # defaults are virtual


# Fetch items as lookups or functions.
@pytest.mark.unit
def test__dictionary06():
    static_dfl = datetime.datetime.now()
    d = Dictionary(dfl=static_dfl, key="value")
    assert d("key") == d["key"] == "value"
    assert d("unk") == d["unk"] == static_dfl


# Existing keys don't fallback to defaults.
@pytest.mark.unit
def test__dictionary07():
    dynamic_dfl = datetime.datetime.now
    static_dfl = dynamic_dfl()
    d = Dictionary(dfl=static_dfl, key="value")
    assert d.get("key") == d.get("key", static_dfl) == "value"
    assert d.get("key") == d.get("key", dynamic_dfl) == "value"
    assert d.get("key") == d.get("key", None) == "value"


# Dynamic defaults overwrite static defaults.
@pytest.mark.unit
def test__dictionary08():
    dynamic_dfl = datetime.datetime.now
    static_dfl = dynamic_dfl()
    d = Dictionary(dfl=static_dfl, key="value")
    assert d.get("unk") != d.get("unk", dynamic_dfl)
    assert d.get("unk", static_dfl) == static_dfl
    assert d.get("unk", None) is None
    assert d.get("unk", 5) == 5
    assert d.get("unk", dynamic_dfl) != d.get("unk", static_dfl)   # overwrite static default
    assert d.get("unk", dynamic_dfl) != d.get("unk", dynamic_dfl)  # dynamic called each time.


@pytest.fixture
def regular_dict() -> dict:
    return {'key1': "value", 'key2': 2}
