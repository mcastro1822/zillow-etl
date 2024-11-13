"""
Blocks used in Zillow ETL
"""

from prefecto.blocks import lazy_load

from zillow.mongodb import MongoDB


class Blocks:
    """Class for lazy loading Prefect Blocks."""

    # Define the block name variables
    mongo_block: str = "mongodb-dev"

    @property
    @lazy_load("mongo_block")
    def mongodb(self) -> MongoDB:
        """The password block."""


blocks = Blocks()
