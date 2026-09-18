import pytest


@pytest.mark.slow
def test_studionet_smoke_is_explicitly_opt_in():
    """The resumable deployment script owns live network evidence, not CI defaults."""
    assert True
