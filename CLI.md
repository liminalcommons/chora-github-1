---
title: GitHub - CLI Reference
type: reference
status: active
last_updated: '2025-11-14'
tags:
- documentation
- reference
---

# GitHub - CLI Reference

**Command**: `github`
**Interface**: Click (Python)
**Version**: 0.1.0

---

## Installation

```bash
# Install from PyPI
pip install github

# Install from source
git clone https://github.com/your-org/github.git
cd github
pip install -e .
```

---

## Global Options

All commands support these global options:

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--format` | `-f` | Output format (json, table, yaml) | `json` |
| `--version` | | Show version and exit | |
| `--help` | `-h` | Show help message | |

---

## Commands

### create

Create a new github entity.

**Usage**:
```bash
github create NAME [OPTIONS]
```

**Arguments**:
- `NAME` - Entity name (required, 1-200 characters)

**Options**:
- `--description, -d TEXT` - Entity description
- `--metadata, -m KEY=VALUE` - Metadata key-value pairs (can be specified multiple times)

**Examples**:
```bash
# Simple creation
github create "My Task"

# With description
github create "My Task" --description "Important work"

# With metadata
github create "My Task" \
  --metadata priority=high \
  --metadata assignee=alice

# Table output
github create "My Task" --format table
```

**Output** (JSON):
```json
{
  "success": true,
  "message": "Entity created successfully",
  "entity": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "My Task",
    "description": null,
    "status": "pending",
    "metadata": {},
    "created_at": "2025-01-01T12:00:00Z",
    "updated_at": "2025-01-01T12:00:00Z"
  }
}
```

---

### get

Get a specific entity by ID.

**Usage**:
```bash
github get ENTITY_ID
```

**Arguments**:
- `ENTITY_ID` - UUID of the entity to retrieve

**Examples**:
```bash
# Get entity
github get 550e8400-e29b-41d4-a716-446655440000

# Table format
github get 550e8400-e29b-41d4-a716-446655440000 --format table

# YAML format
github get 550e8400-e29b-41d4-a716-446655440000 --format yaml
```

**Output** (JSON):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "My Task",
  "description": null,
  "status": "pending",
  "metadata": {},
  "created_at": "2025-01-01T12:00:00Z",
  "updated_at": "2025-01-01T12:00:00Z"
}
```

**Errors**:
- `NOT_FOUND` - Entity does not exist
- `INVALID_UUID` - Malformed UUID

---

### list

List all entities with optional filtering and pagination.

**Usage**:
```bash
github list [OPTIONS]
```

**Options**:
- `--status, -s STATUS` - Filter by status (pending, active, completed, failed)
- `--name-contains, -n TEXT` - Filter by name substring (case-insensitive)
- `--offset INT` - Pagination offset (default: 0)
- `--limit, -l INT` - Max results to return (default: 100)

**Examples**:
```bash
# List all
github list

# Filter by status
github list --status active

# Filter by name
github list --name-contains "task"

# Pagination
github list --offset 20 --limit 10

# Table format
github list --format table

# Combine filters
github list --status active --name-contains "urgent" --limit 5
```

**Output** (JSON):
```json
{
  "entities": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Task 1",
      "status": "active",
      "created_at": "2025-01-01T12:00:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "name": "Task 2",
      "status": "pending",
      "created_at": "2025-01-01T13:00:00Z"
    }
  ],
  "total": 2,
  "offset": 0,
  "limit": 100
}
```

**Output** (Table):
```
ID                                    Name     Status   Created
550e8400-e29b-41d4-a716-446655440000  Task 1   active   2025-01-01 12:00:00
660e8400-e29b-41d4-a716-446655440001  Task 2   pending  2025-01-01 13:00:00

Total: 2 entities
```

---

### update

Update an existing entity.

**Usage**:
```bash
github update ENTITY_ID [OPTIONS]
```

**Arguments**:
- `ENTITY_ID` - UUID of the entity to update

**Options**:
- `--name, -n TEXT` - New name
- `--description, -d TEXT` - New description
- `--metadata, -m KEY=VALUE` - Metadata to add/update (can be specified multiple times)

**Examples**:
```bash
# Update name
github update 550e8400-e29b-41d4-a716-446655440000 --name "Updated Task"

# Update description
github update 550e8400-e29b-41d4-a716-446655440000 \
  --description "New description"

# Update multiple fields
github update 550e8400-e29b-41d4-a716-446655440000 \
  --name "Updated" \
  --description "New desc" \
  --metadata priority=low

# Clear description (set to null)
github update 550e8400-e29b-41d4-a716-446655440000 --description ""
```

**Output** (JSON):
```json
{
  "success": true,
  "message": "Entity updated successfully",
  "entity": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Updated Task",
    "description": "New description",
    "status": "pending",
    "metadata": {"priority": "low"},
    "created_at": "2025-01-01T12:00:00Z",
    "updated_at": "2025-01-01T14:00:00Z"
  }
}
```

**Errors**:
- `NOT_FOUND` - Entity does not exist
- `VALIDATION_ERROR` - Invalid field values

---

### delete

Delete an entity.

**Usage**:
```bash
github delete ENTITY_ID
```

**Arguments**:
- `ENTITY_ID` - UUID of the entity to delete

**Examples**:
```bash
# Delete entity
github delete 550e8400-e29b-41d4-a716-446655440000

# Confirm deletion
github get 550e8400-e29b-41d4-a716-446655440000
# Error: NOT_FOUND
```

**Output** (JSON):
```json
{
  "success": true,
  "message": "Entity deleted successfully"
}
```

**Errors**:
- `NOT_FOUND` - Entity does not exist

---

### status

Update entity status.

**Usage**:
```bash
github status ENTITY_ID NEW_STATUS
```

**Arguments**:
- `ENTITY_ID` - UUID of the entity
- `NEW_STATUS` - New status (pending, active, completed, failed)

**Status Transitions**:
```
pending → active → completed
    ↓        ↓
  failed   failed
```

**Examples**:
```bash
# Activate entity
github status 550e8400-e29b-41d4-a716-446655440000 active

# Mark as completed
github status 550e8400-e29b-41d4-a716-446655440000 completed

# Mark as failed
github status 550e8400-e29b-41d4-a716-446655440000 failed
```

**Output** (JSON):
```json
{
  "success": true,
  "message": "Status updated to active",
  "entity": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "My Task",
    "status": "active",
    "updated_at": "2025-01-01T15:00:00Z"
  }
}
```

**Errors**:
- `NOT_FOUND` - Entity does not exist
- `INVALID_STATUS` - Invalid status value
- `VALIDATION_ERROR` - Invalid status transition (e.g., completed → active)

---

### health

Check service health.

**Usage**:
```bash
github health
```

**Examples**:
```bash
# Check health
github health

# Table format
github health --format table
```

**Output** (JSON):
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2025-01-01T16:00:00Z"
}
```

---

## Output Formats

### JSON (default)

```bash
github list --format json
```

**Characteristics**:
- Machine-readable
- Full field output
- ISO 8601 timestamps
- Suitable for scripting

---

### Table

```bash
github list --format table
```

**Characteristics**:
- Human-readable
- Column-aligned
- Truncated for readability
- Color-coded (success=green, error=red, warning=yellow)

**Example**:
```
ID                                    Name          Status   Created
550e8400-e29b-41d4-a716-446655440000  My Task       active   2025-01-01 12:00
660e8400-e29b-41d4-a716-446655440001  Another Task  pending  2025-01-01 13:00

Total: 2 entities
```

---

### YAML

```bash
github list --format yaml
```

**Characteristics**:
- Human-readable
- Full field output
- Indented structure
- Suitable for configuration

**Example**:
```yaml
entities:
  - id: 550e8400-e29b-41d4-a716-446655440000
    name: My Task
    status: active
    created_at: '2025-01-01T12:00:00Z'
  - id: 660e8400-e29b-41d4-a716-446655440001
    name: Another Task
    status: pending
    created_at: '2025-01-01T13:00:00Z'
total: 2
```

---

## Error Handling

**Exit Codes**:
- `0` - Success
- `1` - General error
- `2` - Validation error
- `3` - Not found error
- `4` - Configuration error

**Error Output Format**:
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Name must be between 1 and 200 characters",
  "details": {
    "field": "name",
    "constraint": "length",
    "min": 1,
    "max": 200
  }
}
```

**Table Format Errors**:
```
❌ Error: VALIDATION_ERROR
Name must be between 1 and 200 characters
```

---

## Scripting Examples

### Bash Script - Bulk Create

```bash
#!/bin/bash
# Create multiple entities from a file

while IFS= read -r name; do
  github create "$name" --format json | \
    jq -r '.entity.id'
done < tasks.txt
```

### Bash Script - Status Report

```bash
#!/bin/bash
# Count entities by status

for status in pending active completed failed; do
  count=$(github list --status $status --format json | jq '.total')
  echo "$status: $count"
done
```

### Python Script - Process Entities

```python
import subprocess
import json

# Get all active entities
result = subprocess.run(
    ["github", "list", "--status", "active", "--format", "json"],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)

for entity in data["entities"]:
    print(f"Processing: {entity['name']}")
    # Process entity...
```

---

## Environment Variables

- `GITHUB_LOG_LEVEL` - Set logging level (DEBUG, INFO, WARNING, ERROR)
- `GITHUB_CONFIG_PATH` - Path to configuration file
- `NO_COLOR` - Disable colored output (set to any value)

**Examples**:
```bash
# Debug logging
export GITHUB_LOG_LEVEL=DEBUG
github create "Task"

# Disable colors
export NO_COLOR=1
github list --format table
```

---

## Configuration File

**Location**: `~/.github/config.yaml`

**Example**:
```yaml
# Default output format
format: table

# Pagination defaults
pagination:
  limit: 50
  offset: 0

# Logging
logging:
  level: INFO
  file: ~/.github/logs/cli.log
```

---

## Troubleshooting

### Command Not Found

```bash
# Ensure package is installed
pip list | grep github

# Reinstall if needed
pip install --force-reinstall github
```

### Invalid UUID Error

```bash
# UUIDs must be in format: 550e8400-e29b-41d4-a716-446655440000
# Check UUID format
echo "550e8400-e29b-41d4-a716-446655440000" | grep -E '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
```

### Permission Errors

```bash
# Check file permissions
ls -la ~/.github/

# Fix permissions
chmod 755 ~/.github/
```

---

## See Also

- **[API.md](API.md)** - REST API reference
- **[AGENTS.md](AGENTS.md)** - Agent awareness guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Architecture documentation

---

**Generated by**: chora-base SAP-047 Capability Server Template
