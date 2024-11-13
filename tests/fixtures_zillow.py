from pathlib import Path

import orjson
import polars as pl
import pytest
from bs4 import BeautifulSoup
from pytest import FixtureRequest


@pytest.fixture
def grab_html(asset_folder, request: FixtureRequest) -> bytes:
    """ """
    path: Path = asset_folder / "response" / request.param

    with open(path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")
        return soup.encode("utf-8")


@pytest.fixture
def grab_json(asset_folder, request: FixtureRequest) -> dict:
    """ """
    path: Path = asset_folder / "response" / request.param

    with open(path, "r", encoding="utf-8") as file:
        results = orjson.loads(file.read())
        return results


@pytest.fixture
def grab_parquet(asset_folder, request: FixtureRequest) -> dict:
    """ """
    path: Path = asset_folder / "transform" / request.param

    return pl.read_parquet(path)
