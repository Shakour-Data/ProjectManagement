from Project_Management.input_handler import InputHandler

input_handler = InputHandler()

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

    inputs = input_handler.read_json_files()
    if inputs is None:
        print("Failed to load input files. Please check the input directory and JSON files.")
        return

    # Placeholder for processing inputs and managing project
    print(f"Loaded input files: {list(inputs.keys())}")
    print("Starting project management automation...")
    # TODO: Implement task management, GitHub integration, progress tracking, reporting, etc.

def status():
    """
    Show current status of the project management tool.
    """
    print("Project Management Tool is installed and ready.")
    # TODO: Implement status reporting based on current project state
