from pydantic import BaseModel, Field
from typing import Optional

class WBSLevel(BaseModel):
    id: str
    name: str
    parent_id: Optional[str] = None
    duration_days: Optional[int] = None

class Resource(BaseModel):
    id: str
    name: str
    type: str
    availability: Optional[int] = None

class Allocation(BaseModel):
    wbs_id: str
    resource_id: str
    allocation_percentage: float = Field(..., ge=0, le=100)

class ProjectStartDate(BaseModel):
    start_date: str  # ISO format date string
