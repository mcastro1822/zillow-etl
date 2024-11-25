"""
Module to manage query creation
"""

import httpx
from fake_useragent import UserAgent
from prefect import task
from pydantic import BaseModel, Field

from zillow.mongo_models.query_config import RegionConfig


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
    headers = {"User-Agent": UserAgent().random, "csrfToken": csrf_token}
    client: httpx.Client = httpx.Client()

    if page_num is None:
        page_num = 1

    payload = Payload.from_config(region_config, page_num)

    r: httpx.Response = client.put(
        "https://www.zillow.com/async-create-search-page-state",
        headers=headers,
        json=payload,
    )

    r.raise_for_status()

    return r.json()


@task(name="Parse First Page")
def parse_max_pages(first_page_json: dict) -> int:
    """
    Returns the max page length from first page

    Args:
        first_page_json: dict

    Returns:
        total_pages: Total count of paginated pages
    """
