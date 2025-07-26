from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import json

router = APIRouter()

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'SystemInputs', 'user_inputs')

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

@router.get("/user_inputs/wbs_levels")
def get_wbs_levels():
    path = os.path.join(DATA_DIR, 'wbs_levels.json')
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@router.post("/user_inputs/wbs_levels")
def save_wbs_levels(levels: List[WBSLevel]):
    path = os.path.join(DATA_DIR, 'wbs_levels.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump([level.dict() for level in levels], f, ensure_ascii=False, indent=2)
    return {"message": "WBS levels saved successfully"}

@router.get("/user_inputs/resources")
def get_resources():
    path = os.path.join(DATA_DIR, 'resources.json')
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@router.post("/user_inputs/resources")
def save_resources(resources: List[Resource]):
    path = os.path.join(DATA_DIR, 'resources.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump([resource.dict() for resource in resources], f, ensure_ascii=False, indent=2)
    return {"message": "Resources saved successfully"}

@router.get("/user_inputs/allocations")
def get_allocations():
    path = os.path.join(DATA_DIR, 'allocations.json')
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@router.post("/user_inputs/allocations")
def save_allocations(allocations: List[Allocation]):
    path = os.path.join(DATA_DIR, 'allocations.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump([allocation.dict() for allocation in allocations], f, ensure_ascii=False, indent=2)
    return {"message": "Allocations saved successfully"}

@router.get("/user_inputs/project_start_date")
def get_project_start_date():
    path = os.path.join(DATA_DIR, 'project_start_date.json')
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@router.post("/user_inputs/project_start_date")
def save_project_start_date(start_date: ProjectStartDate):
    path = os.path.join(DATA_DIR, 'project_start_date.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(start_date.dict(), f, ensure_ascii=False, indent=2)
    return {"message": "Project start date saved successfully"}
