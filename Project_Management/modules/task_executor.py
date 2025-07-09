from src.task_management import TaskManagement

def main():
    tm = TaskManagement()
    # Generate WBS from a sample project idea
    tm.generate_wbs_from_idea("Complete Project Management Tool")

    # Calculate urgency and importance and prioritize tasks
    prioritized_tasks = tm.prioritize_tasks()

    # List top 10 tasks by priority
    top_10_tasks = prioritized_tasks[:10]

    print("Top 10 tasks by priority (importance and urgency):")
    for i, task in enumerate(top_10_tasks, 1):
        print(f"{i}. Task ID: {task.id}, Title: {task.title}, Importance: {task.importance:.2f}, Urgency: {task.urgency:.2f}")

    # Simulate executing tasks one by one
    for task in top_10_tasks:
        print(f"Executing Task ID {task.id}: {task.title}")
        # Here you could add code to mark task as in_progress or completed
        task.status = "completed"
        print(f"Task ID {task.id} completed.")

    # List next 10 tasks by priority (11-20)
    next_10_tasks = prioritized_tasks[10:20]

    print("\nNext 10 tasks by priority (importance and urgency):")
    for i, task in enumerate(next_10_tasks, 11):
        print(f"{i}. Task ID: {task.id}, Title: {task.title}, Importance: {task.importance:.2f}, Urgency: {task.urgency:.2f}")

    # Simulate executing next 10 tasks one by one
    for task in next_10_tasks:
        print(f"Executing Task ID {task.id}: {task.title}")
        task.status = "completed"
        print(f"Task ID {task.id} completed.")

if __name__ == "__main__":
    main()
