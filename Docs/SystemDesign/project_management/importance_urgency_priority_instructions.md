Importance Urgency Priority Instructions



# Priority, Urgency, and Eisenhower Matrix Instructions

This document describes the methodology implemented in the project management tool for calculating task priority, urgency, and classification using the Eisenhower matrix, as outlined in the detailed implementation plan.

---

## Priority and Urgency Calculation

* Priority (Importance) is calculated based on multiple weighted factors including:
* Task dependencies
* Critical path involvement
* Schedule and cost impact
* Stakeholder priority and risk complexity
* Resource availability and quality impact
* Milestone roles and bottleneck potential
* Reusability frequency
* Urgency is calculated based on factors such as:
* Deadline proximity
* Next activity dependencies
* Risk of delay and immediate decision requirements
* Stakeholder pressure and limited resource time
* Competitive advantage and critical issue fixes
* External schedule coordination and compensatory costs
* Both priority and urgency scores are normalized on a scale from 0 to 100.
* For leaf tasks, scores are calculated directly from these factors.
* For parent tasks, scores are aggregated from their subtasks, typically by averaging.

---

## Eisenhower Matrix Classification

Tasks are classified into four quadrants based on their priority and urgency scores:

| Quadrant | Priority (Importance) | Urgency | Action |
| --- | --- | --- | --- |
| Do Now | High (≥ 70) | High (≥ 70) | Immediate attention |
| Schedule | High (≥ 70) | Low (< 70) | Plan and schedule |
| Delegate | Low (< 70) | High (≥ 70) | Assign to others |
| Eliminate | Low (< 70) | Low (< 70) | Consider dropping |

---

## Usage in the Project Management Tool

* The tool automatically calculates these scores based on task metadata and project data.
* Tasks are prioritized and scheduled accordingly.
* The Eisenhower matrix helps focus on critical tasks and optimize resource allocation.
* Scores and classifications are saved in JSON files for reporting and visualization.
* Reports include top tasks in each Eisenhower quadrant.
* Visual dashboards summarize task priorities and urgencies.

---

## Reference

This methodology is implemented as described in the detailed implementation plan located at:

`projects/current_project/docs/detailed_implementation_plan.txt`

---

This document ensures alignment between the code implementation and project documentation for priority and urgency calculations and task classification.