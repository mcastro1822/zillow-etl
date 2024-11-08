from prefect import flow


@flow
def queue_listings(state_code: str):
    """
    Queues listings to scrape via state

    Args:
        state_code: Two character state abbreviation to supply


    """
