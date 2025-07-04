import pytest
from src import progress_report
from src.task_management import TaskManagement

def test_generate_importance_urgency_report():
    tm = TaskManagement()
    tm.generate_wbs_from_idea("Test Project")
    progress_report.generate_importance_urgency_report(tm)
    # Check if the report file is created and contains expected sections
    with open(progress_report.IMPORTANCE_URGENCY_REPORT_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "Importance and Urgency Report" in content
    assert "Top 10 Important Tasks" in content
    assert "Top 10 Urgent Tasks" in content
    assert "- Importance:" in content
    assert "- Urgency:" in content
    assert "- Status:" in content
    assert "- Description:" in content
