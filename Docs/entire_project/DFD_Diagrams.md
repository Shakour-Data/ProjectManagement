# Data Flow Diagrams (DFD) for Project Management Software

This document contains Data Flow Diagrams (DFD) at levels 0, 1, 2, and 3 for the project management software, updated with standard DFD symbols and additional data stores, processes, and data flows as per feedback.

---

## Legend

- **Process:** Rounded rectangle
- **Data Store:** Open-ended rectangle
- **External Entity:** Simple rectangle
- **Data Flow:** Arrow with label

---

## Level 0 DFD - Context Diagram

```mermaid
graph TD
    User[/"User"/]
    System[/"Project Management System"/]

    User -->|User Inputs| System
    System -->|Reports & Notifications| User

    %% Data Stores
    TaskDB[(Task Database)]
    UserProfiles[(User Profiles)]
    BackupStorage[(Backup Storage)]

    System --> TaskDB
    System --> UserProfiles
    System --> BackupStorage
```

---

## Level 1 DFD - High-Level Processes

```mermaid
graph TD
    User[/"User"/]
    InputHandler((Input Handling))
    TaskManagement((Task Management))
    CommitAutomation((Commit Automation))
    BackupManager((Backup Management))
    GitRepo[/"Git Repository"/]
    Reporting((Reporting and Dashboard))

    TaskDB[(Task Database)]
    UserPrefs[(User Preferences)]
    BackupStorage[(Backup Storage)]
    ConfigStore[(Configuration Store)]

    User -->|Submit Inputs| InputHandler
    InputHandler -->|Processed Data| TaskManagement
    TaskManagement -->|Task Updates| CommitAutomation
    CommitAutomation -->|Commits and Pushes| GitRepo
    CommitAutomation -->|Backup Data| BackupManager
    TaskManagement -->|Progress Data| Reporting
    Reporting -->|Reports| User

    %% Data Stores connections
    TaskManagement --> TaskDB
    InputHandler --> UserPrefs
    BackupManager --> BackupStorage
    InputHandler --> ConfigStore

    %% User Management Processes
    Auth((Authentication))
    UserProfileMgmt((User Profile Management))
    AccessControl((Access Control))

    User --> Auth
    Auth --> UserProfileMgmt
    UserProfileMgmt --> AccessControl
    AccessControl --> InputHandler

    %% Error and Feedback Flows
    InputHandler -->|Error Feedback| User
    BackupManager -->|Backup Status| Reporting
```

---

## Level 2 DFD - Detailed Task Management and Commit Automation

```mermaid
graph TD
    User[/"User"/]
    InputHandler((Input Handler))
    TaskParser((Task Parser))
    WBSGenerator((WBS Generator))
    UrgencyImportanceCalc((Urgency and Importance Calculator))
    TaskScheduler((Task Scheduler))
    CommitMsgGenerator((Commit Message Generator))
    GitInterface[/"Git Interface"/]
    BackupManager((Backup Manager))
    CommitTaskDB[(Commit Task Database)]
    Reporting((Reporting Module))

    User -->|User Inputs| InputHandler
    InputHandler -->|Parsed Input Data| TaskParser
    TaskParser -->|WBS Data| WBSGenerator
    WBSGenerator -->|Urgency and Importance Data| UrgencyImportanceCalc
    UrgencyImportanceCalc -->|Scheduled Tasks| TaskScheduler
    TaskScheduler -->|Task Progress Data| Reporting
    TaskScheduler -->|Commit Instructions| CommitMsgGenerator
    CommitMsgGenerator -->|Commit Commands| GitInterface
    GitInterface -->|Commit Records| CommitTaskDB
    CommitMsgGenerator -->|Backup Data| BackupManager
    CommitTaskDB -->|Progress Reports| Reporting
    Reporting -->|Reports| User

    %% Data Stores
    TaskDB[(Task Database)]
    UserPrefs[(User Preferences)]
    BackupStorage[(Backup Storage)]

    TaskScheduler --> TaskDB
    InputHandler --> UserPrefs
    BackupManager --> BackupStorage

    %% Error Handling and Feedback
    InputHandler -->|Error Feedback| User
```

---

## Level 3 DFD - Task Scheduler Detailed Processes

```mermaid
graph TD
    TaskScheduler((Task Scheduler))
    PriorityCalc((Priority Calculation))
    ConflictDetection((Conflict Detection))
    TaskAssignment((Task Assignment))
    TaskCompletion((Task Completion))
    ScheduleOutput((Schedule Output))

    TaskScheduler -->|Task Data| PriorityCalc
    TaskScheduler -->|Task Data| ConflictDetection
    TaskScheduler -->|Task Data| TaskAssignment
    TaskScheduler -->|Task Data| TaskCompletion
    PriorityCalc -->|Priority Scores| ScheduleOutput
    ConflictDetection -->|Conflict Reports| ScheduleOutput
    TaskAssignment -->|Assignment Details| ScheduleOutput
    TaskCompletion -->|Completion Status| ScheduleOutput
```

---

## Level 3 DFD - Commit Message Generator Detailed Processes

```mermaid
graph TD
    CommitMsgGenerator((Commit Message Generator))
    ChangeCategorization((Change Categorization))
    CommitMsgCreation((Commit Message Creation))
    CommitValidation((Commit Validation))
    CommitExecution((Commit Execution))
    BackupTrigger((Backup Trigger))

    CommitMsgGenerator -->|Change Data| ChangeCategorization
    CommitMsgGenerator -->|Commit Messages| CommitMsgCreation
    CommitMsgGenerator -->|Validation Results| CommitValidation
    CommitMsgGenerator -->|Commit Commands| CommitExecution
    CommitMsgGenerator -->|Backup Signals| BackupTrigger
```

---

## Level 3 DFD - Input Handler Detailed Processes

```mermaid
graph TD
    InputHandler((Input Handler))
    InputValidation((Input Validation))
    DataParsing((Data Parsing))
    ErrorHandling((Error Handling))
    DataForwarding((Data Forwarding))

    InputHandler -->|Raw Input Data| InputValidation
    InputHandler -->|Validated Data| DataParsing
    InputHandler -->|Error Reports| ErrorHandling
    InputHandler -->|Parsed Data| DataForwarding
    ErrorHandling -->|Error Feedback| User
```

---

## Level 3 DFD - Reporting Module Detailed Processes

```mermaid
graph TD
    Reporting((Reporting Module))
    DataAggregation((Data Aggregation))
    ReportGeneration((Report Generation))
    ReportDelivery((Report Delivery))

    Reporting -->|Aggregated Data| DataAggregation
    Reporting -->|Report Templates| ReportGeneration
    Reporting -->|Final Reports| ReportDelivery
```

---

*Note:* The diagrams represent the main data flows and processes based on the current understanding of the software architecture and modules. Data stores are represented as open rectangles, processes as rounded rectangles, and external entities as simple rectangles.
