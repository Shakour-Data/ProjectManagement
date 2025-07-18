import json
from pathlib import Path

class InputHandler:
    def __init__(self, input_dir='project_inputs/PM_JSON/user_inputs'):
        self.input_dir = Path(input_dir)

    def ensure_input_dir(self):
        if not self.input_dir.exists():
            self.input_dir.mkdir()
            print(f"Created input directory at {self.input_dir.resolve()}")
        else:
            print(f"Input directory already exists at {self.input_dir.resolve()}")

    def read_json_files(self):
        if not self.input_dir.exists():
            print(f"Input directory {self.input_dir.resolve()} does not exist.")
            return None

        json_files = list(self.input_dir.glob('*.json'))
        if not json_files:
            print(f"No JSON input files found in {self.input_dir.resolve()}.")
            return None

        # First validate all JSON files for correctness
        for jf in json_files:
            try:
                with open(jf, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                print(f"JSON decode error in file {jf.name}: {e}")
                return None
            except Exception as e:
                print(f"Failed to read {jf.name}: {e}")
                return None

        # If all files are valid, load and return their contents
        inputs = {}
        for jf in json_files:
            with open(jf, 'r', encoding='utf-8') as f:
                inputs[jf.name] = json.load(f)
        return inputs

    def set_input_dir(self, new_dir):
        self.input_dir = Path(new_dir)
        print(f"Input directory set to {self.input_dir.resolve()}")
