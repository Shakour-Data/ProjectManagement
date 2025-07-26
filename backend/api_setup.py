from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import subprocess
import shutil

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = BASE_DIR  # Assuming project root is one level above backend/

@router.post("/setup/init_git")
def init_git_repo():
    git_dir = os.path.join(PROJECT_DIR, ".git")
    if os.path.exists(git_dir):
        return {"message": "Git repository already initialized."}
    try:
        subprocess.run(["git", "init"], cwd=PROJECT_DIR, check=True)
        return {"message": "Git repository initialized."}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Git init failed: {str(e)}")

@router.post("/setup/create_gitignore")
def create_gitignore():
    gitignore_path = os.path.join(PROJECT_DIR, ".gitignore")
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
            f.write("\\n".join(lines) + "\\n")
        return {"message": ".gitignore updated to exclude virtual environment directories."}
    else:
        return {"message": ".gitignore already excludes virtual environment directories."}

@router.post("/setup/create_requirements")
def create_requirements():
    requirements_path = os.path.join(PROJECT_DIR, "requirements.txt")
    if not os.path.exists(requirements_path):
        with open(requirements_path, "w") as f:
            f.write("# Add your project dependencies here\\n")
        return {"message": "requirements.txt created."}
    else:
        return {"message": "requirements.txt already exists."}

@router.post("/setup/create_virtualenv")
def create_virtualenv():
    venv_path = os.path.join(PROJECT_DIR, "venv")
    if os.path.exists(venv_path):
        return {"message": "Virtual environment already exists."}
    try:
        import venv
        venv.create(venv_path, with_pip=True)
        return {"message": "Virtual environment created."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Virtualenv creation failed: {str(e)}")

@router.post("/setup/install_dependencies")
def install_dependencies():
    venv_path = os.path.join(PROJECT_DIR, "venv")
    pip_executable = os.path.join(venv_path, "bin", "pip")
    requirements_path = os.path.join(PROJECT_DIR, "requirements.txt")
    if not os.path.exists(pip_executable):
        raise HTTPException(status_code=500, detail="pip not found in virtual environment.")
    if not os.path.exists(requirements_path):
        return {"message": "requirements.txt not found. Skipping dependency installation."}
    try:
        subprocess.run([pip_executable, "install", "-r", requirements_path], check=True)
        return {"message": "Dependencies installed."}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Dependency installation failed: {str(e)}")

@router.post("/upload/json_file")
async def upload_json_file(file: UploadFile = File(...), target_dir: str = ""):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files are allowed.")
    base_dir = os.path.join(PROJECT_DIR, "project_inputs", "PM_JSON", "user_inputs")
    save_dir = os.path.join(base_dir, target_dir)
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, file.filename)
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        return {"message": f"File {file.filename} uploaded successfully to {target_dir}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@router.get("/upload/expected_files")
def get_expected_files():
    # This could be enhanced to dynamically read expected files from config or docs
    expected_files = [
        {"filename": "level1.json", "path": "wbs_parts/Level1"},
        {"filename": "level2.json", "path": "wbs_parts/Level2"},
        {"filename": "level3.json", "path": "wbs_parts/Level3"},
        {"filename": "human_resources.json", "path": ""},
        {"filename": "task_resource_allocation.json", "path": ""},
    ]
    return expected_files
