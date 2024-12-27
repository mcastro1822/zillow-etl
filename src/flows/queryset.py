"""
This module queries a set of property attibutes by city
"""

import pendulum
import polars as pl
from prefect import flow, task, unmapped
from prefect.futures import PrefectFuture
from prefecto.concurrency import BatchTask

from zillow.mongo_models.query_config import RegionConfig
from zillow.query import parse_max_pages, parse_result_content, query_search
from zillow.sitemap import extract_csrf_token


@task(name="Extract and Transform")
def extract_and_transform(page_num, csrf_token, region_config) -> pl.DataFrame:
    """
    Queries region and transforms json to df

    Args:

        region_config: Static attributes for a region

    """
    r_json: dict = query_search.submit(csrf_token, region_config, page_num).result()

    price_results: pl.DataFrame = parse_result_content.submit(r_json).result()

    return price_results


@flow(
    name="Query Zillow Regions", description="Requests a Search from defined boundaries"
)
def query_zillow_regions(region_config: RegionConfig) -> pl.DataFrame:
    """
    Requests a Search from defined boundaries

    # TODO: Dump df into object store

    Args:

        region_config: Static attributes for a region
        recently_modified: Recently modified results from sitemap

    """

    csrf_token = extract_csrf_token()

    first_page: dict = query_search(csrf_token, region_config)

    pages: list[int] = parse_max_pages(first_page)

    batch_get = BatchTask(extract_and_transform, 10)

    futures: list[PrefectFuture] = batch_get.map(
        pages, unmapped(csrf_token), unmapped(region_config)
    )

    results: list = [future.result() for future in futures]

    df: pl.DataFrame = (
        pl.concat(results, how="vertical")
        .with_columns(as_of_date=pl.lit(pendulum.today().date()))
        .cast({"zpid": pl.String})
    )

    return df
