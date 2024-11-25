"""
This module queries a set of property attibutes by city
"""

from zillow.mongo_models.query_config import RegionConfig


def query_zillow_regions(region_config: RegionConfig):
    """
    region_config: Static attributes for a region

    """
    ...
    # csrf_token = extract_csrf_token()

    # Task that calls query and parses the max page count, M. Add to list

    # BatchTask that calls all other 2,....M pages. Add to list

    # BatchTask transformation function and return concat df

    # Dump df into object store
