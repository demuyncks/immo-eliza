from typing import Optional

from pydantic import BaseModel


class Property(BaseModel):
    zip_code: str
    province: str
    region: str
    type_of_property: str
    subtype_of_property: str
    type_of_sale: str
    number_of_rooms: int
    living_area: float
    fully_equipped_kitchen: str
    furnished: bool
    open_fire: bool
    terrace: bool
    terrace_area: Optional[float] = 0.0
    garden: bool
    garden_area: Optional[float] = 0.0
    surface_of_the_land: float
    number_of_facades: int
    swimming_pool: bool
    state_of_the_building: str
