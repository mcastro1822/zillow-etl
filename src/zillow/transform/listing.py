import polars as pl
from prefect import task

from zillow.property_model import Property


@task(description="Converts Property Model to Dataframe")
def property_json_to_df(property_json: dict) -> pl.DataFrame:
    """
    Converts incoming property json to polars dataframe

    Args:
        property_json: json of property key value pairs

    Returns:
        df
    """
    property = Property.model_validate(property_json.get("property")).model_dump()

    df: pl.DataFrame = pl.from_dict(property).unnest("resoFacts").unnest("address")

    return df
