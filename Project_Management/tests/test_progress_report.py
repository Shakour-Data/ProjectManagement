import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import progress_report
from task_management import TaskManagement

def test_generate_progress_report():
    tm = TaskManagement()
    tm.generate_wbs_from_idea("Test Project")
    progress_report.generate_report(tm)
    # Check if the report file is created and contains expected sections
    with open(progress_report.DASHBOARD_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "Progress Report" in content
    assert "Completed Activities" in content
    assert "In-Progress Activities" in content
    assert "Pending Activities" in content

def test_progress_report_contains_urgency_importance():
    tm = TaskManagement()
    tm.generate_wbs_from_idea("Test Project")
    progress_report.generate_report(tm)
    with open(progress_report.DASHBOARD_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "Urgency" in content
    assert "Importance" in content
