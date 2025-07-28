from typing import List, Optional
from backend.repositories.project_repository import ProjectRepository
from backend.api_inputs import WBSLevel, Resource, Allocation, ProjectStartDate

class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def list_projects(self) -> List[str]:
        return self.repository.list_projects()

    def create_project(self, project_id: str) -> bool:
        return self.repository.create_project(project_id)

    def delete_project(self, project_id: str) -> bool:
        return self.repository.delete_project(project_id)

    def get_wbs_levels(self, project_id: str) -> List[dict]:
        data = self.repository.read_json_file(project_id, 'wbs_levels.json')
        return data if data else []

    def save_wbs_levels(self, project_id: str, levels: List[WBSLevel]) -> None:
        data = [level.dict() for level in levels]
        self.repository.write_json_file(project_id, 'wbs_levels.json', data)

    def delete_wbs_levels(self, project_id: str) -> bool:
        return self.repository.delete_file(project_id, 'wbs_levels.json')

    def get_resources(self, project_id: str) -> List[dict]:
        data = self.repository.read_json_file(project_id, 'resources.json')
        return data if data else []

    def save_resources(self, project_id: str, resources: List[Resource]) -> None:
        data = [resource.dict() for resource in resources]
        self.repository.write_json_file(project_id, 'resources.json', data)

    def delete_resources(self, project_id: str) -> bool:
        return self.repository.delete_file(project_id, 'resources.json')

    def get_allocations(self, project_id: str) -> List[dict]:
        data = self.repository.read_json_file(project_id, 'allocations.json')
        return data if data else []

    def save_allocations(self, project_id: str, allocations: List[Allocation]) -> None:
        data = [allocation.dict() for allocation in allocations]
        self.repository.write_json_file(project_id, 'allocations.json', data)

    def delete_allocations(self, project_id: str) -> bool:
        return self.repository.delete_file(project_id, 'allocations.json')

    def get_project_start_date(self, project_id: str) -> dict:
        data = self.repository.read_json_file(project_id, 'project_start_date.json')
        return data if data else {}

    def save_project_start_date(self, project_id: str, start_date: ProjectStartDate) -> None:
        self.repository.write_json_file(project_id, 'project_start_date.json', start_date.dict())
