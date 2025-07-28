import os
import json
import shutil
from typing import List, Optional

class ProjectRepository:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    def get_project_path(self, project_id: str) -> str:
        if not project_id or any(c in project_id for c in ['..', '/', '\\']):
            raise ValueError("Invalid project_id")
        return os.path.join(self.base_dir, project_id)

    def list_projects(self) -> List[str]:
        if not os.path.exists(self.base_dir):
            return []
        return [name for name in os.listdir(self.base_dir) if os.path.isdir(os.path.join(self.base_dir, name))]

    def create_project(self, project_id: str) -> bool:
        path = self.get_project_path(project_id)
        if os.path.exists(path):
            return False
        os.makedirs(path)
        return True

    def delete_project(self, project_id: str) -> bool:
        path = self.get_project_path(project_id)
        if not os.path.exists(path):
            return False
        shutil.rmtree(path)
        return True

    def read_json_file(self, project_id: str, filename: str) -> Optional[dict]:
        path = os.path.join(self.get_project_path(project_id), filename)
        if not os.path.exists(path):
            return None
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def write_json_file(self, project_id: str, filename: str, data: dict) -> None:
        path = os.path.join(self.get_project_path(project_id), filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def delete_file(self, project_id: str, filename: str) -> bool:
        path = os.path.join(self.get_project_path(project_id), filename)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False
