from typing import Optional

from pydantic import BaseModel


class DealerSchema(BaseModel):
    dealer_id: str
    dealer_name: str
    dealer_phone: str
    dealer_email: Optional[str]
    dealer_address: str
    dealer_link: Optional[str]


class RegionSchema(BaseModel):
    region_id: str
    region_name: str
    dealers: list[DealerSchema]
