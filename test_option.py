import pytest

def test__lib_option():

    # Determine if wrapper defines something or not.
    assert Something(0).is_defined()
    assert not Nothing().is_defined()

    # Comparisons between other entities.
    assert Something(0) == Something(-2 + 2)    # content equal
    assert Something(0) != Something(1)         # value diff
    assert Something(0) != Something("0")       # type diff
    assert Something(0) != Nothing()            # definition diff
    assert Nothing() == Nothing()               # undefined equals

    # Factory construction
    assert Option(0) == Something(0)
    assert Option() == Nothing()
    assert Option() == Option()

    # Gracefully fetch values if defined.
    assert Something(0).get() == 0
    assert not Nothing().get()

    # Gracefully transform defined values as per the function.
    assert Nothing().map(lambda x: x + 1) == Nothing()
    assert Something(0).map(lambda x: x + 1) == Something(1)
    with pytest.raises(Exception):
        assert Something(0).map(lambda x: 1/x)
    assert Something(1).map_try(lambda x: 1/1) == Something(1)
    assert Something(0).map_try(lambda x: 1/x) == Nothing()
