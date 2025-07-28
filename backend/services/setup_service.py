import os
import subprocess
import logging
from fastapi import UploadFile

logger = logging.getLogger("backend.setup_service")

class SetupService:
    def __init__(self, project_dir: str):
        self.project_dir = project_dir

    def init_git_repo(self) -> str:
        git_dir = os.path.join(self.project_dir, ".git")
        if os.path.exists(git_dir):
            return "Git repository already initialized."
        try:
            subprocess.run(["git", "init"], cwd=self.project_dir, check=True)
            logger.info("Git repository initialized.")
            return "Git repository initialized."
        except subprocess.CalledProcessError as e:
            logger.error(f"Git init failed: {e}")
            raise RuntimeError(f"Git init failed: {str(e)}")

    def create_gitignore(self) -> str:
        gitignore_path = os.path.join(self.project_dir, ".gitignore")
        venv_dirs = ['venv/', '.venv/', 'ENV/', 'env/']
        lines = []
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r") as f:
                lines = f.read().splitlines()
        updated = False
        for venv_dir in venv_dirs:
            if venv_dir not in lines:
                lines.append(venv_dir)
                updated = True
        if updated:
            with open(gitignore_path, "w") as f:
                f.write("\n".join(lines) + "\n")
            logger.info(".gitignore updated to exclude virtual environment directories.")
            return ".gitignore updated to exclude virtual environment directories."
        else:
            logger.info(".gitignore already excludes virtual environment directories.")
            return ".gitignore already excludes virtual environment directories."

    def create_requirements(self) -> str:
        requirements_path = os.path.join(self.project_dir, "requirements.txt")
        if not os.path.exists(requirements_path):
            with open(requirements_path, "w") as f:
                f.write("# Add your project dependencies here\n")
            logger.info("requirements.txt created.")
            return "requirements.txt created."
        else:
            logger.info("requirements.txt already exists.")
            return "requirements.txt already exists."

    def create_virtualenv(self) -> str:
        venv_path = os.path.join(self.project_dir, "venv")
        if os.path.exists(venv_path):
            return "Virtual environment already exists."
        try:
            import venv
            venv.create(venv_path, with_pip=True)
            logger.info("Virtual environment created.")
            return "Virtual environment created."
        except Exception as e:
            logger.error(f"Virtualenv creation failed: {e}")
            raise RuntimeError(f"Virtualenv creation failed: {str(e)}")

    def install_dependencies(self) -> str:
        venv_path = os.path.join(self.project_dir, "venv")
        pip_executable = os.path.join(venv_path, "bin", "pip")
        requirements_path = os.path.join(self.project_dir, "requirements.txt")
        if not os.path.exists(pip_executable):
            logger.error("pip not found in virtual environment.")
            raise RuntimeError("pip not found in virtual environment.")
        if not os.path.exists(requirements_path):
            logger.info("requirements.txt not found. Skipping dependency installation.")
            return "requirements.txt not found. Skipping dependency installation."
        try:
            subprocess.run([pip_executable, "install", "-r", requirements_path], check=True)
            logger.info("Dependencies installed.")
            return "Dependencies installed."
        except subprocess.CalledProcessError as e:
            logger.error(f"Dependency installation failed: {e}")
            raise RuntimeError(f"Dependency installation failed: {str(e)}")

    async def upload_json_file(self, file: UploadFile, target_dir: str = "") -> str:
        if not file.filename.endswith(".json"):
            logger.error("Only JSON files are allowed.")
            raise ValueError("Only JSON files are allowed.")
        base_dir = os.path.join(self.project_dir, "project_inputs", "PM_JSON", "user_inputs")
        save_dir = os.path.join(base_dir, target_dir)
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, file.filename)
        try:
            contents = await file.read()
            with open(file_path, "wb") as f:
                f.write(contents)
            logger.info(f"File {file.filename} uploaded successfully to {target_dir}.")
            return f"File {file.filename} uploaded successfully to {target_dir}."
        except Exception as e:
            logger.error(f"File upload failed: {e}")
            raise RuntimeError(f"File upload failed: {str(e)}")

    def get_expected_files(self):
        # This could be enhanced to dynamically read expected files from config or docs
        expected_files = [
            {"filename": "level1.json", "path": "wbs_parts/Level1"},
            {"filename": "level2.json", "path": "wbs_parts/Level2"},
            {"filename": "level3.json", "path": "wbs_parts/Level3"},
            {"filename": "human_resources.json", "path": ""},
            {"filename": "task_resource_allocation.json", "path": ""},
        ]
        return expected_files
