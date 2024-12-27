"""
Model for query payload
"""

from pydantic import BaseModel, Field

from zillow.mongo_models.db import AbstractRepo, BaseDocument, DocumentSet


class RegionSelection(BaseModel):
    """
    Region Selection Model
    """

    regionId: int = Field(
        name="Region ID", description="Zillow Region ID", examples=[12447]
    )
    regionType: int = Field(
        name="Region Type", description="Zillow Region Type", examples=[6]
    )


class MapBounds(BaseModel):
    """
    Map bounds defintion model
    """

    west: float = Field(
        name="West",
        description="Location based coordinate for boundary definition",
        examples=[-118.668176],
    )
    east: float = Field(
        name="East",
        description="Location based coordinate for boundary definition",
        examples=[-118.155289],
    )
    south: float = Field(
        name="South",
        description="Location based coordinate for boundary definition",
        examples=[33.703652],
    )
    north: float = Field(
        name="North",
        description="Location based coordinate for boundary definition",
        examples=[34.337306],
    )


class RegionConfig(BaseDocument):
    """
    Payload Model
    """

    pagination: dict | None = Field(
        name="Pagination", description="Contains pagaination metadata", default=None
    )

    mapBounds: MapBounds = Field(name="Map Bounds", description="Map Bounds Definition")
    usersSearchTerm: str = Field(
        name="User Search Term",
        description="User query",
        examples=["Los Angeles, CA", "San Diego, CA"],
    )
    regionSelection: list[RegionSelection] = Field(
        name="Region Selection", description="Zillow Region Selections"
    )
    filterState: dict = Field(
        name="Filter State",
        description="Query Filters",
        examples=[{"sortSelection": {"value": "globalrelevanceex"}}],
    )


class RegionSet(DocumentSet):
    """
    Region Set Model for collection
    """

    root: list[RegionConfig]


class RegionDefinitionsRepo(AbstractRepo(RegionConfig, RegionSet, "config_zillow")): ...
