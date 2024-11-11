from prefect import flow
from prefect.futures import PrefectFuture
from prefecto.concurrency import BatchTask

from zillow.extract.site_map_index import collect_sitemap_partitions
from zillow.sitemap import extract_sitemap_dir_urls, extract_sitemap_urls


@flow(name="Queue Zillow Property Listings")
def queue_listings(state_code: str):
    """
    Queues listings to scrape via state

    Args:
        state_code: Two character state abbreviation to supply


    """
    sitemap_dir_html: bytes = extract_sitemap_dir_urls()

    sitemap_partitions: list = collect_sitemap_partitions(sitemap_dir_html)

    batch_get = BatchTask(extract_sitemap_urls, 4)

    futures: list[PrefectFuture] = batch_get.map(sitemap_partitions)

    property_urls = [future.result() for future in futures]

    return property_urls
