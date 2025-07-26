from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from backend.api_inputs import router as inputs_router
from backend.api_setup import router as setup_router

app = FastAPI()

# Allow CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'SystemInputs', 'system_generated')

def load_json(filename: str):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"{filename} not found")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.get("/api/progress_report")
def get_progress_report():
    return load_json('progress_report.json')

@app.get("/api/priority_urgency_report")
def get_priority_urgency_report():
    return load_json('priority_urgency_report.json')

@app.get("/api/cost_management_report")
def get_cost_management_report():
    return load_json('cost_management_report.json')

@app.get("/api/resource_allocation_report")
def get_resource_allocation_report():
    return load_json('resource_allocation_report.json')

@app.get("/api/risk_management_report")
def get_risk_management_report():
    return load_json('risk_management_report.json')

app.include_router(inputs_router)
app.include_router(setup_router)
