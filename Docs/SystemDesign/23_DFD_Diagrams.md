# Data Flow Diagrams (DFD)

## Level 0 DFD

The Level 0 DFD provides a high-level overview of the Project Management system, showing the main processes and data flows:

```
+----------------+        +----------------+        +----------------+
|     User       | -----> |    Frontend    | -----> |   Backend API  |
+----------------+        +----------------+        +----------------+
                                                        |
                                                        v
                                               +----------------+
                                               |   Database     |
                                               +----------------+
                                                        |
                                                        v
                                               +----------------+
                                               |  Reports &     |
                                               |  Dashboards    |
                                               +----------------+
                                                        |
                                                        v
                                               +----------------+
                                               |     User       |
                                               +----------------+
```

## Level 1 DFD

The Level 1 DFD breaks down the Backend processes:

```
+---------------------+      +---------------------+      +---------------------+      +---------------------+
|   Task Management    | ---> | Resource Allocation | ---> |  Progress Tracking  | ---> |      Reporting       |
+---------------------+      +---------------------+      +---------------------+      +---------------------+
```

(Data stores: Project Database, Task Database, Resource Database)

## Detailed DFDs

### Task Management Process

```
User -> Frontend -> Backend API -> Validate -> Store in Task Database -> Notify Progress & Reporting
```

### Resource Allocation Process

```
User -> Frontend -> Backend API -> Validate Resource -> Update Allocation Records -> Notify Reporting
```

### Progress Tracking Process

```
Monitor Task Status -> Calculate Progress -> Update Reports
```

### Reporting Process

```
Aggregate Data -> Generate Reports -> Provide to Frontend
```
