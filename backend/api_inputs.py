from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import json
from fastapi import Query

router = APIRouter()

BASE_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'SystemInputs', 'user_inputs')

def get_project_dir(project_id: str):
    return os.path.join(BASE_DATA_DIR, project_id)

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

@router.get("/projects")
def list_projects():
    if not os.path.exists(BASE_DATA_DIR):
        return []
    projects = [name for name in os.listdir(BASE_DATA_DIR) if os.path.isdir(os.path.join(BASE_DATA_DIR, name))]
    return projects

@router.post("/projects")
def create_project(project_id: str = Query(..., description="Unique project identifier")):
    project_path = get_project_dir(project_id)
    if os.path.exists(project_path):
        return {"message": f"Project '{project_id}' already exists."}
    os.makedirs(project_path)
    return {"message": f"Project '{project_id}' created successfully."}

@router.delete("/projects")
def delete_project(project_id: str = Query(..., description="Unique project identifier")):
    project_path = get_project_dir(project_id)
    if not os.path.exists(project_path):
        return {"message": f"Project '{project_id}' does not exist."}
    import shutil
    shutil.rmtree(project_path)
    return {"message": f"Project '{project_id}' deleted successfully."}

@router.get("/user_inputs/wbs_levels")
def get_wbs_levels(project_id: str = Query(..., description="Project identifier")):
    project_path = get_project_dir(project_id)
    path = os.path.join(project_path, 'wbs_levels.json')
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@router.post("/user_inputs/wbs_levels")
def save_wbs_levels(levels: List[WBSLevel], project_id: str = Query(..., description="Project identifier")):
    project_path = get_project_dir(project_id)
    path = os.path.join(project_path, 'wbs_levels.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump([level.dict() for level in levels], f, ensure_ascii=False, indent=2)
    return {"message": "WBS levels saved successfully"}

@router.delete("/user_inputs/wbs_levels")
def delete_wbs_levels(project_id: str = Query(..., description="Project identifier")):
    project_path = get_project_dir(project_id)
    path = os.path.join(project_path, 'wbs_levels.json')
    if os.path.exists(path):
        os.remove(path)
        return {"message": "WBS levels deleted successfully"}
    return {"message": "WBS levels file not found"}

@router.get("/user_inputs/resources")
def get_resources(project_id: str = Query(..., description="Project identifier")):
    project_path = get_project_dir(project_id)
    path = os.path.join(project_path, 'resources.json')
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@router.post("/user_inputs/resources")
def save_resources(resources: List[Resource], project_id: str = Query(..., description="Project identifier")):
    project_path = get_project_dir(project_id)
    path = os.path.join(project_path, 'resources.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump([resource.dict() for resource in resources], f, ensure_ascii=False, indent=2)
    return {"message": "Resources saved successfully"}

@router.delete("/user_inputs/resources")
def delete_resources(project_id: str = Query(..., description="Project identifier")):
    project_path = get_project_dir(project_id)
    path = os.path.join(project_path, 'resources.json')
    if os.path.exists(path):
        os.remove(path)
        return {"message": "Resources deleted successfully"}
    return {"message": "Resources file not found"}

@router.get("/user_inputs/allocations")
def get_allocations(project_id: str = Query(..., description="Project identifier")):
    project_path = get_project_dir(project_id)
    path = os.path.join(project_path, 'allocations.json')
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@router.post("/user_inputs/allocations")
def save_allocations(allocations: List[Allocation], project_id: str = Query(..., description="Project identifier")):
    project_path = get_project_dir(project_id)
    path = os.path.join(project_path, 'allocations.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump([allocation.dict() for allocation in allocations], f, ensure_ascii=False, indent=2)
    return {"message": "Allocations saved successfully"}

@router.delete("/user_inputs/allocations")
def delete_allocations(project_id: str = Query(..., description="Project identifier")):
    project_path = get_project_dir(project_id)
    path = os.path.join(project_path, 'allocations.json')
    if os.path.exists(path):
        os.remove(path)
        return {"message": "Allocations deleted successfully"}
    return {"message": "Allocations file not found"}

@router.get("/user_inputs/project_start_date")
def get_project_start_date(project_id: str = Query(..., description="Project identifier")):
    project_path = get_project_dir(project_id)
    path = os.path.join(project_path, 'project_start_date.json')
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@router.post("/user_inputs/project_start_date")
def save_project_start_date(start_date: ProjectStartDate, project_id: str = Query(..., description="Project identifier")):
    project_path = get_project_dir(project_id)
    path = os.path.join(project_path, 'project_start_date.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(start_date.dict(), f, ensure_ascii=False, indent=2)
    return {"message": "Project start date saved successfully"}

@router.post("/user_inputs/aggregate_wbs")
def aggregate_wbs(project_id: str = Query(..., description="Project identifier")):
    import glob

    project_path = get_project_dir(project_id)
    wbs_parts_dir = os.path.join(project_path, 'wbs_parts')

    if not os.path.exists(wbs_parts_dir):
        return {"message": "WBS parts directory not found", "success": False}

    aggregated_wbs = []

    # Recursively find all JSON files in wbs_parts_dir
    for filepath in glob.glob(os.path.join(wbs_parts_dir, '**', '*.json'), recursive=True):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                aggregated_wbs.append(data)
        except Exception as e:
            return {"message": f"Failed to read {filepath}: {str(e)}", "success": False}

    # Save aggregated WBS to detailed_wbs.json
    detailed_wbs_path = os.path.join(project_path, 'detailed_wbs.json')
    try:
        with open(detailed_wbs_path, 'w', encoding='utf-8') as f:
            json.dump(aggregated_wbs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return {"message": f"Failed to save detailed_wbs.json: {str(e)}", "success": False}

    return {"message": "Aggregated detailed_wbs.json created successfully", "success": True}
