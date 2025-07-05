import re
import json

def parse_detailed_implementation_plan(filepath):
    """
    Parses the detailed_implementation_plan.txt file to extract a hierarchical WBS structure.
    Returns a list of tasks with nested subtasks.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    wbs = []
    stack = []  # To keep track of current parent tasks by level

    task_pattern = re.compile(r'^(\d+(\.\d+)*)\s+(.*)$')

    for line in lines:
        line = line.strip()
        if not line:
            continue
        match = task_pattern.match(line)
        if match:
            level_str = match.group(1)
            title = match.group(3).strip()
            level = level_str.count('.') + 1

            task = {
                'id': level_str,
                'title': title,
                'level': level,
                'subtasks': []
            }

            # Adjust stack to current level
            while stack and stack[-1]['level'] >= level:
                stack.pop()

            if stack:
                # Add as subtask to last item in stack
                stack[-1]['subtasks'].append(task)
            else:
                # Top level task
                wbs.append(task)

            stack.append(task)

    return wbs

def save_wbs_to_json(wbs, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(wbs, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    import os
    input_path = os.path.join(os.path.dirname(__file__), '../docs/project_management/detailed_implementation_plan.txt')
    output_path = os.path.join(os.path.dirname(__file__), '../docs/project_management/wbs_data.json')
    wbs = parse_detailed_implementation_plan(input_path)
    save_wbs_to_json(wbs, output_path)
    print(f"WBS data parsed and saved to {output_path}")
