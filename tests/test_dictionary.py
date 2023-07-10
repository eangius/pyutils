#!usr/bin/env python

import pytest
import datetime
from lib.dictionary import *


def test__lib_dictionary():

    dynamic_dfl = datetime.datetime.now
    static_dfl = dynamic_dfl()
    d = Dictionary(dfl=static_dfl, key="value")

    # Drop-in regular dictionary behaviour.
    assert isinstance(Dictionary(), dict)
    assert Dictionary() == {}
    assert Dictionary(key1="value", key2=2) == {'key1': "value", 'key2': 2}
    assert Dictionary(dfl=static_dfl) == {}  # defaults are virtual

    # Fetch items as lookups or functions.
    assert d("key") == d["key"] == "value"
    assert d("unk") == d["unk"] == static_dfl

    # Existing keys don't fallback to defaults.
    assert d.get("key") == d.get("key", static_dfl) == "value"
    assert d.get("key") == d.get("key", dynamic_dfl) == "value"
    assert d.get("key") == d.get("key", None) == "value"

    # Dynamic defaults overwrite static defaults.
    assert d.get("unk") != d.get("unk", dynamic_dfl)
    assert d.get("unk", static_dfl) == static_dfl
    assert d.get("unk", None) == static_dfl
    assert d.get("unk", 5) == 5
    assert d.get("unk", dynamic_dfl) != d.get("unk", static_dfl)   # overwrite static default
    assert d.get("unk", dynamic_dfl) != d.get("unk", dynamic_dfl)  # dynamic called each time.



