"""
Prefect Fixtures
"""

import pytest
from prefect.blocks.core import Block
from prefect.testing.utilities import prefect_test_harness

from zillow.mongodb import MongoDB


@pytest.fixture(autouse=True, scope="session")
def prefect_test_fixture():
    with prefect_test_harness():
        yield


def _save_block_(block: Block):
    """
    Saves block to local prefect harness
    """

    block.save(block._block_document_name, overwrite=True)
    return block


@pytest.fixture(autouse=True, scope="session")
def populate_prefect_blocks(prefect_test_fixture):

    mongo_block = MongoDB(
        _block_document_name="mongodb-production",
        host="mongodb://localhost/",
        username="test-username",
        password="test-password",
    )
    _save_block_(mongo_block)

    yield
