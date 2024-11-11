import polars as pl
from prefect import task

from zillow.property_model import Property


@task(description="Converts Property Model to Dataframe")
def property_json_to_df(property_json: dict):
    """ """
    property = Property.model_validate(property_json.get("property")).model_dump()

    df: pl.DataFrame = pl.from_dict(property).unnest("resoFacts").unnest("address")
    # df.write_parquet('property.parquet', compression='snappy')
    return df
