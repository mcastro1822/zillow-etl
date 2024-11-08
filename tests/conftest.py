from pathlib import Path

import pytest


@pytest.fixture
def asset_folder():
    """
    Project Test asset folder path
    """

    return Path(__file__).parent / "assets"
