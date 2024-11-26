"""
Module to manage query creation
"""

import random
import time

import httpx
import polars as pl
from fake_useragent import UserAgent
from prefect import task
from pydantic import BaseModel, Field

from flows.utility import modify_param_on_retry
from zillow.mongo_models.query_config import RegionConfig
from zillow.searchset.query_model import ResultSet


class Payload(BaseModel):
    """
    Base Model for query payload
    """

    searchQueryState: RegionConfig = Field(
        name="Search Query State", description="Search query parameters"
    )
    wants: dict = Field(
        name="Wants",
        description="Search Query Result Formatting",
        default={"cat1": ["listResults"], "cat2": ["total"]},
    )

    @classmethod
    def from_config(cls, region_config: RegionConfig, page_num: int):
        """
        Creates a payload for a given region config

        Args:
            region_config: MongoDB static query parameters
            page_num: page number of pagination set to query
        """

        region_config_dump: dict = region_config.model_dump()

        region_config_dump.update({"pagination": {"currentPage": page_num}})

        region_config = RegionConfig.model_validate(region_config_dump)

        return cls(
            searchQueryState=region_config,
        )


@task(name="Query Search", description="Calls a page from zillow's result set")
def query_search(
    csrf_token: str, region_config: RegionConfig, page_num: int | None = None
):
    """
    Sends a search query to zillow
    """

    sleep_time: int = random.randint(30, 60)
    time.sleep(sleep_time)

    csrf_token = modify_param_on_retry(csrf_token)

    headers = {"User-Agent": UserAgent().random, "csrfToken": csrf_token}
    client: httpx.Client = httpx.Client()

    if page_num is None:
        page_num = 1

    payload = Payload.from_config(region_config, page_num).model_dump()

    r: httpx.Response = client.put(
        "https://www.zillow.com/async-create-search-page-state",
        headers=headers,
        json=payload,
        timeout=120,
    )

    r.raise_for_status()

    return r.json()


@task(name="Parse First Page")
def parse_max_pages(first_page_json: dict) -> list[int]:
    """
    Returns the max page length from first page

    Args:
        first_page_json: dict

    Returns:
        total_pages: Total count of paginated pages
    """

    pages: int = first_page_json.get("cat1").get("searchList").get("totalPages")

    return [i for i in range(1, pages + 1)]


@task(name="Parse Page Content")
def parse_result_content(page_json: dict) -> list[int]:
    """
    Returns the max page length from first page

    Args:
        first_page_json: dict

    Returns:
        total_pages: Total count of paginated pages
    """
    data: list = page_json.get("cat1").get("searchResults").get("listResults")

    results = list(map(ResultSet.model_validate, data))

    df = pl.from_dicts(results).rename({"unformattedPrice": "price"})

    return df
