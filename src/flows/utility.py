"""
Utility Functions
"""

import random
import time
from typing import Callable

from prefect.client.schemas import State, TaskRun
from prefect.context import get_run_context
from prefect.futures import PrefectFuture
from prefecto.concurrency import BatchTask
from prefecto.logging import get_prefect_or_default_logger

from zillow.sitemap import extract_csrf_token


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
        sleep_time: int = random.randint(30, 70)
        time.sleep(sleep_time)

        return csrf_token


def batch_task_results(func: Callable, objects: list, size: int | None = None) -> list:
    """
    Runs a prefecto Batch Task over a callable and some collection of objects

    Args:
        func: Prefect Task
        objects: List of items to iterate over
        size (Optional): Size of the batch

    Returns:
        results: Batch task results
    """

    if not size:
        size = 10

    batch_get = BatchTask(func, size)

    futures: list[PrefectFuture] = batch_get.map(objects)

    results: list = [future.result() for future in futures]

    return results
