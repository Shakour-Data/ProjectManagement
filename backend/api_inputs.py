import logging
from fastapi import APIRouter, HTTPException, Query
from typing import List
import os
import json
from backend.repositories.project_repository import ProjectRepository
from backend.services.project_service import ProjectService
from project_management.modules.gantt_chart_data import GanttChartData
from fastapi.responses import JSONResponse
from backend.models import WBSLevel, Resource, Allocation, ProjectStartDate

router = APIRouter(prefix="/api/v1")

logger = logging.getLogger("backend.api_inputs")
logging.basicConfig(level=logging.INFO)

BASE_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'SystemInputs', 'user_inputs')

project_repository = ProjectRepository(BASE_DATA_DIR)
project_service = ProjectService(project_repository)

@router.get("/projects")
def list_projects():
    try:
        return project_service.list_projects()
    except Exception as e:
        logger.error(f"Error listing projects: {e}")
        raise HTTPException(status_code=500, detail="Failed to list projects")

@router.post("/projects")
def create_project(project_id: str = Query(..., description="Unique project identifier")):
    try:
        created = project_service.create_project(project_id)
        if not created:
            return {"message": f"Project '{project_id}' already exists."}
        logger.info(f"Project created: {project_id}")
        return {"message": f"Project '{project_id}' created successfully."}
    except Exception as e:
        logger.error(f"Error creating project '{project_id}': {e}")
        raise HTTPException(status_code=500, detail="Failed to create project")

@router.delete("/projects")
def delete_project(project_id: str = Query(..., description="Unique project identifier")):
    try:
        deleted = project_service.delete_project(project_id)
        if not deleted:
            return {"message": f"Project '{project_id}' does not exist."}
        logger.info(f"Project deleted: {project_id}")
        return {"message": f"Project '{project_id}' deleted successfully."}
    except Exception as e:
        logger.error(f"Error deleting project '{project_id}': {e}")
        raise HTTPException(status_code=500, detail="Failed to delete project")

@router.get("/user_inputs/wbs_levels")
def get_wbs_levels(project_id: str = Query(..., description="Project identifier")):
    try:
        return project_service.get_wbs_levels(project_id)
    except Exception as e:
        logger.error(f"Error getting WBS levels for project '{project_id}': {e}")
        raise HTTPException(status_code=500, detail="Failed to get WBS levels")

@router.post("/user_inputs/wbs_levels")
def save_wbs_levels(levels: List[WBSLevel], project_id: str = Query(..., description="Project identifier")):
    try:
        project_service.save_wbs_levels(project_id, levels)
        logger.info(f"WBS levels saved for project '{project_id}'")
        return {"message": "WBS levels saved successfully"}
    except Exception as e:
        logger.error(f"Error saving WBS levels for project '{project_id}': {e}")
        raise HTTPException(status_code=500, detail="Failed to save WBS levels")

@router.delete("/user_inputs/wbs_levels")
def delete_wbs_levels(project_id: str = Query(..., description="Project identifier")):
    try:
        deleted = project_service.delete_wbs_levels(project_id)
        if deleted:
            logger.info(f"WBS levels deleted for project '{project_id}'")
            return {"message": "WBS levels deleted successfully"}
        return {"message": "WBS levels file not found"}
    except Exception as e:
        logger.error(f"Error deleting WBS levels for project '{project_id}': {e}")
        raise HTTPException(status_code=500, detail="Failed to delete WBS levels")

@router.get("/user_inputs/resources")
def get_resources(project_id: str = Query(..., description="Project identifier")):
    try:
        return project_service.get_resources(project_id)
    except Exception as e:
        logger.error(f"Error getting resources for project '{project_id}': {e}")
        raise HTTPException(status_code=500, detail="Failed to get resources")

@router.post("/user_inputs/resources")
def save_resources(resources: List[Resource], project_id: str = Query(..., description="Project identifier")):
    try:
        project_service.save_resources(project_id, resources)
        logger.info(f"Resources saved for project '{project_id}'")
        return {"message": "Resources saved successfully"}
    except Exception as e:
        logger.error(f"Error saving resources for project '{project_id}': {e}")
        raise HTTPException(status_code=500, detail="Failed to save resources")

@router.delete("/user_inputs/resources")
def delete_resources(project_id: str = Query(..., description="Project identifier")):
    try:
        deleted = project_service.delete_resources(project_id)
        if deleted:
            logger.info(f"Resources deleted for project '{project_id}'")
            return {"message": "Resources deleted successfully"}
        return {"message": "Resources file not found"}
    except Exception as e:
        logger.error(f"Error deleting resources for project '{project_id}': {e}")
        raise HTTPException(status_code=500, detail="Failed to delete resources")

@router.get("/user_inputs/allocations")
def get_allocations(project_id: str = Query(..., description="Project identifier")):
    try:
        return project_service.get_allocations(project_id)
    except Exception as e:
        logger.error(f"Error getting allocations for project '{project_id}': {e}")
        raise HTTPException(status_code=500, detail="Failed to get allocations")

@router.post("/user_inputs/allocations")
def save_allocations(allocations: List[Allocation], project_id: str = Query(..., description="Project identifier")):
    try:
        project_service.save_allocations(project_id, allocations)
        logger.info(f"Allocations saved for project '{project_id}'")
        return {"message": "Allocations saved successfully"}
    except Exception as e:
        logger.error(f"Error saving allocations for project '{project_id}': {e}")
        raise HTTPException(status_code=500, detail="Failed to save allocations")

@router.delete("/user_inputs/allocations")
def delete_allocations(project_id: str = Query(..., description="Project identifier")):
    try:
        deleted = project_service.delete_allocations(project_id)
        if deleted:
            logger.info(f"Allocations deleted for project '{project_id}'")
            return {"message": "Allocations deleted successfully"}
        return {"message": "Allocations file not found"}
    except Exception as e:
        logger.error(f"Error deleting allocations for project '{project_id}': {e}")
        raise HTTPException(status_code=500, detail="Failed to delete allocations")

@router.get("/user_inputs/project_start_date")
def get_project_start_date(project_id: str = Query(..., description="Project identifier")):
    try:
        return project_service.get_project_start_date(project_id)
    except Exception as e:
        logger.error(f"Error getting project start date for project '{project_id}': {e}")
        raise HTTPException(status_code=500, detail="Failed to get project start date")

@router.post("/user_inputs/project_start_date")
def save_project_start_date(start_date: ProjectStartDate, project_id: str = Query(..., description="Project identifier")):
    try:
        project_service.save_project_start_date(project_id, start_date)
        logger.info(f"Project start date saved for project '{project_id}'")
        return {"message": "Project start date saved successfully"}
    except Exception as e:
        logger.error(f"Error saving project start date for project '{project_id}': {e}")
        raise HTTPException(status_code=500, detail="Failed to save project start date")

@router.post("/user_inputs/aggregate_wbs")
def aggregate_wbs(project_id: str = Query(..., description="Project identifier")):
    import glob
    try:
        project_path = project_repository.get_project_path(project_id)
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
                logger.error(f"Failed to read {filepath}: {e}")
                return {"message": f"Failed to read {filepath}: {str(e)}", "success": False}
        # Save aggregated WBS to detailed_wbs.json
        detailed_wbs_path = os.path.join(project_path, 'detailed_wbs.json')
        try:
            with open(detailed_wbs_path, 'w', encoding='utf-8') as f:
                json.dump(aggregated_wbs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to save detailed_wbs.json: {e}")
            return {"message": f"Failed to save detailed_wbs.json: {str(e)}", "success": False}
        logger.info(f"Aggregated detailed_wbs.json created for project '{project_id}'")
        # Generate Gantt chart data automatically after aggregation
        gantt_generator = GanttChartData(input_dir=os.path.join(project_path))
        gantt_generator.load_tasks()
        gantt_data = gantt_generator.build_gantt_data()
        gantt_output_path = os.path.join(project_path, 'gantt_chart_data.json')
        try:
            with open(gantt_output_path, 'w', encoding='utf-8') as gf:
                json.dump(gantt_data, gf, indent=2, ensure_ascii=False)
            logger.info(f"Gantt chart data saved to {gantt_output_path}")
        except Exception as ge:
            logger.error(f"Failed to save Gantt chart data: {ge}")
            return {"message": f"Failed to save Gantt chart data: {str(ge)}", "success": False}
        return {"message": "Aggregated detailed_wbs.json and Gantt chart data created successfully", "success": True}
    except Exception as e:
        logger.error(f"Error aggregating WBS for project '{project_id}': {e}")
        return {"message": "Failed to aggregate WBS", "success": False}
