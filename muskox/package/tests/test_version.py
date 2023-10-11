import re

from muskox.package import version


def test_version():
    pattern: str = r"^\d+\.\d+\.\d+$"
    assert re.match(pattern, version)
