from pathlib import Path

import pytest

pytest_plugins = ["fixtures_zillow", "fixtures_prefect", "fixtures_mongo"]


@pytest.fixture
def asset_folder() -> Path:
    """
    Project Test asset folder path
    """

    return Path(__file__).parent / "assets"
