import json
from pathlib import Path

class InputHandler:
    def __init__(self, input_dir='PM_Input'):
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

        inputs = {}
        for jf in json_files:
            try:
                with open(jf, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    inputs[jf.name] = data
            except json.JSONDecodeError as e:
                print(f"JSON decode error in file {jf.name}: {e}")
                return None
            except Exception as e:
                print(f"Failed to read {jf.name}: {e}")
                return None
        return inputs

    def set_input_dir(self, new_dir):
        self.input_dir = Path(new_dir)
        print(f"Input directory set to {self.input_dir.resolve()}")
