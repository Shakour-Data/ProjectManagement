# Instructions for Designing JSON Resource Files for Automatic Database Table Creation

This document provides a detailed, standardized guideline for structuring JSON resource files so that they can be automatically mapped to and populate database tables. The instructions are aligned with project management best practices and ensure compatibility with relational database schemas.

---

## 1. Purpose

To enable seamless integration of JSON resource files with database systems by defining a clear, consistent JSON schema that corresponds directly to database table structures. This facilitates automation in data import, validation, and project management workflows.

---

## 2. JSON Structure and Database Mapping Principles

- Each JSON object represents a row in the database table.
- JSON keys correspond to database column names.
- Data types in JSON should align with database column data types (e.g., string, integer, real/float, boolean).
- Hierarchical or nested data should be flattened or stored in related tables with foreign keys.

---

## 3. Defining JSON Keys and Data Types

- Use consistent and descriptive key names matching the database column names.
- Supported data types:
  - **String**: For textual data (e.g., task titles, descriptions).
  - **Integer**: For whole numbers (e.g., IDs, levels).
  - **Real/Float**: For decimal numbers (e.g., progress, importance).
  - **Boolean**: For true/false flags (if applicable).
  - **Array**: For lists of related items (should be handled via related tables or JSON columns if supported).
- Avoid complex nested objects unless the database supports JSON columns.

---

## 4. Handling Hierarchical Data

- For hierarchical data like tasks and subtasks:
  - Use a parent-child relationship with a `parent_id` field referencing the parent task's ID.
  - Alternatively, store subtasks as separate entries with a foreign key to the parent.
- Avoid deeply nested JSON objects for relational databases.

---

## 5. Example JSON Schema for a Tasks Table

```json
[
  {
    "id": "1",
    "title": "Define project scope",
    "description": "Outline the project objectives and deliverables",
    "level": 1,
    "importance": 0.8,
    "urgency": 0.6,
    "status": "Not Started",
    "progress": 0.0,
    "parent_id": null
  },
  {
    "id": "1.1",
    "title": "Gather requirements",
    "description": "Collect detailed requirements from stakeholders",
    "level": 2,
    "importance": 0.9,
    "urgency": 0.7,
    "status": "In Progress",
    "progress": 0.5,
    "parent_id": "1"
  }
]
```

---

## 6. Database Table Schema Correspondence

| Column Name | Data Type | Description                          |
|-------------|-----------|----------------------------------|
| id          | TEXT      | Unique identifier for the task    |
| title       | TEXT      | Task name                        |
| description | TEXT      | Detailed task description         |
| level       | INTEGER   | Hierarchy level in the WBS        |
| importance  | REAL      | Importance score (0.0 to 1.0)     |
| urgency     | REAL      | Urgency score (0.0 to 1.0)        |
| status      | TEXT      | Current status of the task         |
| progress    | REAL      | Completion percentage (0.0 to 1.0)|
| parent_id   | TEXT      | ID of the parent task (nullable)  |

---

## 7. Validation and Synchronization

- Validate JSON files against the defined schema before importing.
- Use automated scripts or ETL tools to parse JSON and insert/update database tables.
- Maintain version control for JSON files to track changes.
- Schedule regular synchronization between JSON resources and database tables.

---

## 8. Best Practices

- Keep JSON files well-formatted and human-readable.
- Use consistent naming conventions for keys and database columns.
- Document the JSON schema and database mapping clearly.
- Handle missing or optional fields gracefully in the database.
- For large datasets, consider batch processing and incremental updates.

---

## 9. Summary

Designing JSON resource files with clear schema definitions aligned to database tables enables efficient automation, data integrity, and project management effectiveness. Following these guidelines ensures that JSON files can be reliably used to create and populate database tables, supporting dynamic project workflows.

For further assistance, please contact the project management office.

---

*Note: Store this document in the main project documentation directory for universal access across projects.*
