# Database Schema

The system uses SQLAlchemy for relational data. For initial phase, SQLite is used, designed for seamless migration to PostgreSQL for Enterprise scalability.

## 1. Entities

### `Workspaces`
A logical boundary for users, teams, or organizations.
- `id`: UUID (PK)
- `name`: String
- `created_at`: DateTime

### `Projects`
A container for a specific goal or set of tasks.
- `id`: UUID (PK)
- `workspace_id`: UUID (FK)
- `name`: String
- `status`: Enum (PLANNING, ACTIVE, PAUSED, COMPLETED)
- `created_at`: DateTime

### `Goals`
The high-level user request.
- `id`: UUID (PK)
- `project_id`: UUID (FK)
- `description`: Text
- `status`: Enum
- `deliverables_expected`: JSON

### `Tasks`
Nodes in the execution DAG.
- `id`: UUID (PK)
- `goal_id`: UUID (FK)
- `description`: Text
- `assigned_agent`: String
- `status`: Enum (PENDING, IN_PROGRESS, WAITING_APPROVAL, COMPLETED, FAILED)
- `dependencies`: JSON (List of Task IDs)
- `result_summary`: Text

### `Memories`
Long-term semantic storage references.
- `id`: UUID (PK)
- `project_id`: UUID (FK)
- `memory_type`: Enum (CONVERSATION, EXTRACTED_FACT, DECISION, USER_PREFERENCE)
- `content`: Text
- `vector_ref_id`: String (Reference to Vector DB)
- `created_at`: DateTime

### `ApprovalRequests`
Pending actions requiring human intervention.
- `id`: UUID (PK)
- `task_id`: UUID (FK)
- `tool_name`: String
- `tool_arguments`: JSON
- `status`: Enum (PENDING, APPROVED, REJECTED)
- `requested_at`: DateTime

## 2. Vector Database (Chroma / Qdrant)
Used for Semantic Memory and Document querying.
Collections:
- `project_{project_id}_documents`: PDF, Word, Excel text chunks.
- `user_preferences`: General rules across all projects.
