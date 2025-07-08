from typing import List, Dict, Any

def top_n_by_importance(tasks: List[Dict[str, Any]], n: int = 10) -> List[Dict[str, Any]]:
    """
    Returns top n tasks sorted by importance descending.
    """
    sorted_tasks = sorted(tasks, key=lambda x: x.get('importance', 0), reverse=True)
    return sorted_tasks[:n]

def top_n_by_urgency(tasks: List[Dict[str, Any]], n: int = 10) -> List[Dict[str, Any]]:
    """
    Returns top n tasks sorted by urgency descending.
    """
    sorted_tasks = sorted(tasks, key=lambda x: x.get('urgency', 0), reverse=True)
    return sorted_tasks[:n]

def eisenhower_matrix(tasks: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Categorizes tasks into Eisenhower matrix quadrants:
    - urgent_important
    - urgent_not_important
    - not_urgent_important
    - not_urgent_not_important
    """
    matrix = {
        'urgent_important': [],
        'urgent_not_important': [],
        'not_urgent_important': [],
        'not_urgent_not_important': []
    }
    for task in tasks:
        urgent = task.get('urgency', 0) >= 0.5
        important = task.get('importance', 0) >= 0.5
        if urgent and important:
            matrix['urgent_important'].append(task)
        elif urgent and not important:
            matrix['urgent_not_important'].append(task)
        elif not urgent and important:
            matrix['not_urgent_important'].append(task)
        else:
            matrix['not_urgent_not_important'].append(task)
    return matrix
