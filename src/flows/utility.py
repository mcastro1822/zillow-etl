"""
Utility Functions
"""

from typing import Callable

from prefect.futures import PrefectFuture
from prefecto.concurrency import BatchTask


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
