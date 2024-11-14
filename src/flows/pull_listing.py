"""
Worker Flow to pull and transform zillow listing
"""

import random
import time

import polars as pl
from prefect import flow, task, unmapped
from prefect.client.schemas import State, TaskRun
from prefect.context import get_run_context
from prefect.futures import PrefectFuture
from prefecto.concurrency import BatchTask
from prefecto.logging import get_prefect_or_default_logger

from zillow.extract.listing import collect_listing_attrs
from zillow.sitemap import extract_csrf_token, extract_listing_url
from zillow.sitemap_model import Property
from zillow.transform.listing import property_json_to_df


def modify_param_on_retry(csrf_token):
    """
    Upon retry a new csrf token will be retrieved
    """
    # Get the current Prefect context

    logger = get_prefect_or_default_logger()
    context = get_run_context()
    tsk_run: TaskRun = context.task_run
    state: State = tsk_run.state

    retry_count = 1 if state.name == "AwaitingRetry" else 0

    if retry_count > 0:
        logger.info(f"Retry attempt {retry_count}: modifying creating new csrf token")
        csrf_token = extract_csrf_token()
        return csrf_token
    else:
        sleep_time: int = random.randint(30, 60)
        time.sleep(sleep_time)

        return csrf_token


@task(name="Collect Listing", description="Collects Listing Datafram")
def listing_collection(property_dict: dict, csrf_token: str) -> pl.DataFrame:
    """
    Handles request, json parse from html, and converstion to dataframe

    Args:
        property_url: URL of the listing
        csrf_token: Token for use across each worker node

    Returns:
        df: Dataframe for the listing
    """

    csrf_token = modify_param_on_retry(csrf_token)

    properties: Property = Property.model_validate(property_dict)

    html_bytes: bytes = extract_listing_url.submit(
        properties.property_url, csrf_token
    ).result()
    listing_json: dict = collect_listing_attrs.submit(html_bytes).result()
    df: pl.DataFrame = property_json_to_df.submit(listing_json).result()

    return df


@flow(name="Query Zillow Listing", description="Collects listing data")
def query_zillow_listings(property_urls: list[dict]):
    """
    Queries Zillow to extract listing json.
    """
    csrf_token = extract_csrf_token()

    batch_get = BatchTask(listing_collection, 4)

    futures: list[PrefectFuture] = batch_get.map(property_urls, unmapped(csrf_token))

    results: list = [future.result() for future in futures]

    df: pl.DataFrame = pl.concat(results, how="diagonal_relaxed")

    return df
