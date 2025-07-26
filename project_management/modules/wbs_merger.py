import os
import json

class WBSMerger:
    def __init__(self, parts_dir='SystemInputs/user_inputs/wbs_parts', output_file='SystemInputs/system_generated/detailed_wbs.json'):
        self.parts_dir = parts_dir
        self.output_file = output_file

    def load_part(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def merge_subtasks(self, base_subtasks, additional_subtasks):
        """
        Merge additional subtasks into base subtasks by matching IDs.
        If a subtask exists in both, merge their subtasks recursively.
        If not, append the additional subtask.
        Also merge extended fields: cost, quality_metrics, risk_factors, resource_assignments.
        """
        base_dict = {subtask['id']: subtask for subtask in base_subtasks}
        for add_subtask in additional_subtasks:
            if add_subtask['id'] in base_dict:
                # Recursive merge
                base_subtask = base_dict[add_subtask['id']]
                # Merge extended fields if present
                for field in ['cost', 'quality_metrics', 'risk_factors', 'resource_assignments']:
                    if field in add_subtask:
                        base_subtask[field] = add_subtask[field]
                if 'subtasks' in add_subtask and add_subtask['subtasks']:
                    if 'subtasks' not in base_subtask:
                        base_subtask['subtasks'] = []
                    base_subtask['subtasks'] = self.merge_subtasks(base_subtask.get('subtasks', []), add_subtask['subtasks'])
            else:
                base_subtasks.append(add_subtask)
        return base_subtasks

    def merge_all_parts(self):
        parts_files = []
        for root, _, files in os.walk(self.parts_dir):
            for file in files:
                if file.endswith('.json'):
                    parts_files.append(os.path.join(root, file))

        if not parts_files:
            print("No WBS parts found in directory.")
            return

        # Load the first part as base
        base_part = self.load_part(parts_files[0])
        for part_file in parts_files[1:]:
            part = self.load_part(part_file)
            # Merge subtasks recursively
            if 'subtasks' in part and part['subtasks']:
                if 'subtasks' not in base_part:
                    base_part['subtasks'] = []
                base_part['subtasks'] = self.merge_subtasks(base_part.get('subtasks', []), part['subtasks'])

        # Save merged detailed WBS
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(base_part, f, indent=2, ensure_ascii=False)
        print(f"Merged detailed WBS saved to {self.output_file}")

if __name__ == "__main__":
    merger = WBSMerger()
    merger.merge_all_parts()
