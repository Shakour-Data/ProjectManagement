import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from backend.services.setup_service import SetupService

router = APIRouter(prefix="/api/v1")

logger = logging.getLogger("backend.api_setup")
logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = BASE_DIR  # Assuming project root is one level above backend/

setup_service = SetupService(PROJECT_DIR)

@router.post("/setup/init_git")
def init_git_repo():
    try:
        message = setup_service.init_git_repo()
        return {"message": message}
    except Exception as e:
        logger.error(f"Git init failed: {e}")
        raise HTTPException(status_code=500, detail=f"Git init failed: {str(e)}")

@router.post("/setup/create_gitignore")
def create_gitignore():
    try:
        message = setup_service.create_gitignore()
        return {"message": message}
    except Exception as e:
        logger.error(f"Create gitignore failed: {e}")
        raise HTTPException(status_code=500, detail=f"Create gitignore failed: {str(e)}")

@router.post("/setup/create_requirements")
def create_requirements():
    try:
        message = setup_service.create_requirements()
        return {"message": message}
    except Exception as e:
        logger.error(f"Create requirements failed: {e}")
        raise HTTPException(status_code=500, detail=f"Create requirements failed: {str(e)}")

@router.post("/setup/create_virtualenv")
def create_virtualenv():
    try:
        message = setup_service.create_virtualenv()
        return {"message": message}
    except Exception as e:
        logger.error(f"Create virtualenv failed: {e}")
        raise HTTPException(status_code=500, detail=f"Create virtualenv failed: {str(e)}")

@router.post("/setup/install_dependencies")
def install_dependencies():
    try:
        message = setup_service.install_dependencies()
        return {"message": message}
    except Exception as e:
        logger.error(f"Install dependencies failed: {e}")
        raise HTTPException(status_code=500, detail=f"Install dependencies failed: {str(e)}")

@router.post("/upload/json_file")
async def upload_json_file(file: UploadFile = File(...), target_dir: str = ""):
    try:
        message = await setup_service.upload_json_file(file, target_dir)
        return {"message": message}
    except ValueError as ve:
        logger.error(f"File upload validation failed: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@router.get("/upload/expected_files")
def get_expected_files():
    try:
        return setup_service.get_expected_files()
    except Exception as e:
        logger.error(f"Get expected files failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get expected files failed: {str(e)}")
