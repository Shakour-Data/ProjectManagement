from modules.input_handler import InputHandler
from modules.setup_automation import SetupAutomation

input_handler = InputHandler()
setup_automation = SetupAutomation()

def install():
    """
    Installation routine for the project management tool.
    Creates PM_Input directory if not exists.
    """
    input_handler.ensure_input_dir()
    print("Installation complete. Please add your JSON input files to the PM_Input directory.")

def start(input_dir=None):
    """
    Start the project management automation.
    Reads JSON input files and performs management operations.
    """
    if input_dir:
        input_handler.set_input_dir(input_dir)

    # Example of automated initial setup question responses
    print("Automated Setup Responses:")
    questions = [
        "What is the git flow used in this project?",
        "What naming conventions should be followed?"
    ]
    for q in questions:
        answer = setup_automation.get_standard_response(q)
        print(f"Q: {q}\nA: {answer}\n")

    inputs = input_handler.read_json_files()
    if inputs is None:
        print("Failed to load input files. Please check the input directory and JSON files.")
        return

    # Process inputs and generate reports
    print(f"Loaded input files: {list(inputs.keys())}")
    print("Starting project management automation...")

    # Import reporting functions
    from modules import reporting

    # Extract tasks from inputs - assuming tasks are in wbs_data.json or detailed_wbs.json
    tasks = []
    if 'wbs_data.json' in inputs:
        tasks = inputs['wbs_data.json']
    elif 'detailed_wbs.json' in inputs:
        tasks = inputs['detailed_wbs.json']

    if not tasks:
        print("No task data found in input files.")
        return

    # Generate top 10 important tasks
    top_important = reporting.top_n_by_importance(tasks, 10)
    print("\nTop 10 Important Tasks:")
    for t in top_important:
        print(f"- {t.get('title', 'No Title')} (Importance: {t.get('importance', 0)})")

    # Generate top 10 urgent tasks
    top_urgent = reporting.top_n_by_urgency(tasks, 10)
    print("\nTop 10 Urgent Tasks:")
    for t in top_urgent:
        print(f"- {t.get('title', 'No Title')} (Urgency: {t.get('urgency', 0)})")

    # Generate Eisenhower matrix
    matrix = reporting.eisenhower_matrix(tasks)
    print("\nEisenhower Matrix:")
    for quadrant, items in matrix.items():
        print(f"\n{quadrant.replace('_', ' ').title()} ({len(items)} tasks):")
        for t in items:
            print(f"  - {t.get('title', 'No Title')} (Importance: {t.get('importance', 0)}, Urgency: {t.get('urgency', 0)})")

def status():
    """
    Show current status of the project management tool.
    """
    print("Project Management Tool is installed and ready.")
    # TODO: Implement status reporting based on current project state
