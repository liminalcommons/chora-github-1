---
title: GitHub - REST API Reference
type: reference
status: active
last_updated: '2025-11-14'
tags:
- documentation
- reference
---

# GitHub - REST API Reference

**Base URL**: `http://localhost:8000`
**Framework**: FastAPI
**OpenAPI**: `http://localhost:8000/docs`
**Version**: 0.1.0

---

## Overview

This REST API provides CRUD operations for github entities with:
- ✅ Full OpenAPI/Swagger documentation
- ✅ JSON request/response format
- ✅ Pagination and filtering
- ✅ Standardized error responses
- ✅ CORS support

---

## Authentication

**Current**: No authentication (development mode)

**Production**: Add authentication middleware as needed (JWT, API keys, OAuth, etc.)

---

## Base Endpoints

### GET /

Get API information.

**Response** (200 OK):
```json
{
  "name": "GitHub API",
  "version": "0.1.0",
  "docs": "http://localhost:8000/docs"
}
```

---

### GET /health

Health check endpoint.

**Response** (200 OK):
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2025-01-01T12:00:00Z"
}
```

---

### GET /docs

Interactive OpenAPI documentation (Swagger UI).

**Usage**: Open in browser: `http://localhost:8000/docs`

---

### GET /openapi.json

OpenAPI schema in JSON format.

**Response** (200 OK):
```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "GitHub API",
    "version": "0.1.0"
  },
  "paths": { ... }
}
```

---

## Entity Endpoints

### POST /api/v1/github/entities

Create a new entity.

**Request Body**:
```json
{
  "name": "Entity Name",
  "description": "Optional description",
  "metadata": {
    "key": "value"
  }
}
```

**Fields**:
- `name` (string, required) - Entity name (1-200 characters)
- `description` (string, optional) - Entity description
- `metadata` (object, optional) - Arbitrary key-value metadata

**Response** (201 Created):
```json
{
  "success": true,
  "message": "Entity created successfully",
  "entity": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Entity Name",
    "description": "Optional description",
    "status": "pending",
    "metadata": {"key": "value"},
    "created_at": "2025-01-01T12:00:00Z",
    "updated_at": "2025-01-01T12:00:00Z"
  }
}
```

**Errors**:
- `400 Bad Request` - Validation error (invalid name, etc.)
- `422 Unprocessable Entity` - Malformed JSON

**Example (curl)**:
```bash
curl -X POST http://localhost:8000/api/v1/github/entities \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Task",
    "description": "Important work",
    "metadata": {"priority": "high"}
  }'
```

---

### GET /api/v1/github/entities/{entity_id}

Get a specific entity by ID.

**Path Parameters**:
- `entity_id` (UUID) - Entity identifier

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Entity Name",
  "description": "Optional description",
  "status": "pending",
  "metadata": {"key": "value"},
  "created_at": "2025-01-01T12:00:00Z",
  "updated_at": "2025-01-01T12:00:00Z"
}
```

**Errors**:
- `404 Not Found` - Entity does not exist
- `422 Unprocessable Entity` - Invalid UUID format

**Example (curl)**:
```bash
curl http://localhost:8000/api/v1/github/entities/550e8400-e29b-41d4-a716-446655440000
```

---

### GET /api/v1/github/entities

List all entities with optional filtering and pagination.

**Query Parameters**:
- `status` (string, optional) - Filter by status (pending, active, completed, failed)
- `name_contains` (string, optional) - Filter by name substring (case-insensitive)
- `offset` (integer, optional, default: 0) - Pagination offset
- `limit` (integer, optional, default: 100) - Maximum results to return

**Response** (200 OK):
```json
{
  "entities": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Entity 1",
      "status": "active",
      "created_at": "2025-01-01T12:00:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "name": "Entity 2",
      "status": "pending",
      "created_at": "2025-01-01T13:00:00Z"
    }
  ],
  "total": 2,
  "offset": 0,
  "limit": 100
}
```

**Errors**:
- `400 Bad Request` - Invalid status value

**Examples (curl)**:
```bash
# List all
curl http://localhost:8000/api/v1/github/entities

# Filter by status
curl "http://localhost:8000/api/v1/github/entities?status=active"

# Filter by name
curl "http://localhost:8000/api/v1/github/entities?name_contains=task"

# Pagination
curl "http://localhost:8000/api/v1/github/entities?offset=20&limit=10"

# Combine filters
curl "http://localhost:8000/api/v1/github/entities?status=active&name_contains=urgent&limit=5"
```

---

### PUT /api/v1/github/entities/{entity_id}

Update an entity (full replacement).

**Path Parameters**:
- `entity_id` (UUID) - Entity identifier

**Request Body**:
```json
{
  "name": "Updated Name",
  "description": "Updated description",
  "metadata": {"updated": true}
}
```

**Fields**:
- `name` (string, optional) - New name
- `description` (string, optional) - New description
- `metadata` (object, optional) - New metadata (replaces existing)

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Entity updated successfully",
  "entity": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Updated Name",
    "description": "Updated description",
    "status": "pending",
    "metadata": {"updated": true},
    "created_at": "2025-01-01T12:00:00Z",
    "updated_at": "2025-01-01T14:00:00Z"
  }
}
```

**Errors**:
- `404 Not Found` - Entity does not exist
- `400 Bad Request` - Validation error
- `422 Unprocessable Entity` - Malformed JSON

**Example (curl)**:
```bash
curl -X PUT http://localhost:8000/api/v1/github/entities/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Task",
    "description": "New description"
  }'
```

---

### PATCH /api/v1/github/entities/{entity_id}

Partially update an entity (only specified fields).

**Path Parameters**:
- `entity_id` (UUID) - Entity identifier

**Request Body**:
```json
{
  "name": "Partially Updated Name"
}
```

**Fields**: Same as PUT, but all fields are optional. Only provided fields are updated.

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Entity updated successfully",
  "entity": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Partially Updated Name",
    "description": "Original description",  // Unchanged
    "status": "pending",
    "metadata": {"original": "metadata"},  // Unchanged
    "created_at": "2025-01-01T12:00:00Z",
    "updated_at": "2025-01-01T15:00:00Z"
  }
}
```

**Errors**:
- `404 Not Found` - Entity does not exist
- `400 Bad Request` - Validation error

**Example (curl)**:
```bash
curl -X PATCH http://localhost:8000/api/v1/github/entities/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{"name": "New Name Only"}'
```

---

### DELETE /api/v1/github/entities/{entity_id}

Delete an entity.

**Path Parameters**:
- `entity_id` (UUID) - Entity identifier

**Response** (204 No Content):
No response body.

**Errors**:
- `404 Not Found` - Entity does not exist

**Example (curl)**:
```bash
curl -X DELETE http://localhost:8000/api/v1/github/entities/550e8400-e29b-41d4-a716-446655440000
```

---

### POST /api/v1/github/entities/{entity_id}/status

Update entity status.

**Path Parameters**:
- `entity_id` (UUID) - Entity identifier

**Request Body**:
```json
{
  "status": "active"
}
```

**Fields**:
- `status` (string, required) - New status (pending, active, completed, failed)

**Status Transitions**:
```
pending → active → completed
    ↓        ↓
  failed   failed
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Status updated to active",
  "entity": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Entity Name",
    "status": "active",
    "updated_at": "2025-01-01T16:00:00Z"
  }
}
```

**Errors**:
- `404 Not Found` - Entity does not exist
- `400 Bad Request` - Invalid status or illegal transition

**Example (curl)**:
```bash
curl -X POST http://localhost:8000/api/v1/github/entities/550e8400-e29b-41d4-a716-446655440000/status \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'
```

---

### POST /api/v1/github/entities/bulk/delete

Bulk delete entities.

**Request Body**:
```json
["550e8400-e29b-41d4-a716-446655440000", "660e8400-e29b-41d4-a716-446655440001"]
```

**Response** (200 OK):
```json
{
  "deleted_count": 2,
  "failed_count": 0,
  "failed_ids": []
}
```

**Example (curl)**:
```bash
curl -X POST http://localhost:8000/api/v1/github/entities/bulk/delete \
  -H "Content-Type: application/json" \
  -d '["550e8400-e29b-41d4-a716-446655440000", "660e8400-e29b-41d4-a716-446655440001"]'
```

---

## Error Responses

All errors follow a standardized format:

```json
{
  "error": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": {
    "field": "field_name",
    "constraint": "constraint_type"
  }
}
```

### HTTP Status Codes

| Code | Name | Description |
|------|------|-------------|
| 200 | OK | Successful request |
| 201 | Created | Entity created successfully |
| 204 | No Content | Successful deletion (no body) |
| 400 | Bad Request | Validation error, invalid input |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | Entity not found |
| 409 | Conflict | Duplicate entity, conflict |
| 422 | Unprocessable Entity | Malformed JSON, invalid UUID |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected server error |
| 504 | Gateway Timeout | Operation timeout |

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid field values |
| `NOT_FOUND` | 404 | Entity does not exist |
| `CONFLICT` | 409 | Duplicate entity |
| `PERMISSION_DENIED` | 403 | Access denied |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `TIMEOUT` | 504 | Operation timeout |
| `SERVICE_ERROR` | 500 | Internal error |

### Error Examples

**Validation Error** (400):
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

**Not Found** (404):
```json
{
  "error": "NOT_FOUND",
  "message": "Entity with ID 550e8400-e29b-41d4-a716-446655440000 not found",
  "details": {
    "entity_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

**Invalid UUID** (422):
```json
{
  "error": "INVALID_UUID",
  "message": "Invalid UUID format: not-a-uuid",
  "details": {
    "field": "entity_id",
    "value": "not-a-uuid"
  }
}
```

---

## CORS

**Development Mode**: All origins allowed (`Access-Control-Allow-Origin: *`)

**Production**: Configure specific origins in settings:
```python
# github/config/settings.py
CORS_ORIGINS = [
    "https://your-frontend.com",
    "https://app.example.com"
]
```

---

## Rate Limiting

**Current**: No rate limiting (development mode)

**Production**: Add rate limiting middleware as needed

**Recommended**: Use FastAPI rate limiting or reverse proxy (nginx, Caddy)

---

## Response Headers

All responses include:
- `Content-Type: application/json` (except 204 No Content)
- `X-Request-Duration: {duration}s` - Request processing time
- `Access-Control-Allow-Origin: *` (CORS, development mode)

**Rate Limiting** (if enabled):
- `X-RateLimit-Limit: {limit}` - Request limit
- `X-RateLimit-Remaining: {remaining}` - Remaining requests
- `X-RateLimit-Reset: {timestamp}` - Reset timestamp
- `Retry-After: {seconds}` - Seconds until retry (429 only)

---

## Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Create entity
response = requests.post(
    f"{BASE_URL}/api/v1/github/entities",
    json={
        "name": "My Task",
        "description": "Important work",
        "metadata": {"priority": "high"}
    }
)
entity = response.json()["entity"]
entity_id = entity["id"]

# Get entity
response = requests.get(
    f"{BASE_URL}/api/v1/github/entities/{entity_id}"
)
entity = response.json()

# List entities
response = requests.get(
    f"{BASE_URL}/api/v1/github/entities",
    params={"status": "active", "limit": 10}
)
entities = response.json()["entities"]

# Update entity
response = requests.put(
    f"{BASE_URL}/api/v1/github/entities/{entity_id}",
    json={"name": "Updated Task"}
)

# Update status
response = requests.post(
    f"{BASE_URL}/api/v1/github/entities/{entity_id}/status",
    json={"status": "active"}
)

# Delete entity
response = requests.delete(
    f"{BASE_URL}/api/v1/github/entities/{entity_id}"
)
assert response.status_code == 204
```

---

## JavaScript/TypeScript Client Example

```typescript
const BASE_URL = "http://localhost:8000";

// Create entity
const createResponse = await fetch(
  `${BASE_URL}/api/v1/github/entities`,
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: "My Task",
      description: "Important work",
      metadata: { priority: "high" }
    })
  }
);
const { entity } = await createResponse.json();

// Get entity
const getResponse = await fetch(
  `${BASE_URL}/api/v1/github/entities/${entity.id}`
);
const entityData = await getResponse.json();

// List entities
const listResponse = await fetch(
  `${BASE_URL}/api/v1/github/entities?status=active&limit=10`
);
const { entities } = await listResponse.json();

// Update entity
const updateResponse = await fetch(
  `${BASE_URL}/api/v1/github/entities/${entity.id}`,
  {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: "Updated Task" })
  }
);

// Delete entity
const deleteResponse = await fetch(
  `${BASE_URL}/api/v1/github/entities/${entity.id}`,
  { method: "DELETE" }
);
```

---

## Running the Server

**Development**:
```bash
uvicorn github.interfaces.rest:app --reload --port 8000
```

**Production** (with Gunicorn):
```bash
gunicorn github.interfaces.rest:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

**Docker**:
```bash
docker build -t github .
docker run -p 8000:8000 github
```

---

---

## MCP Interface (Model Context Protocol)

**Server Name**: `mcp-server-github`
**Version**: 1.0.0
**Namespace**: `github`
**Entry Point**: `github-mcp`

### Overview

The MCP interface provides 8 tools for AI assistants (like Claude) to interact with GitHub repositories. All tools use the `github:` namespace prefix.

**Features**:
- ✅ 8 GitHub tools (issues, PRs, files)
- ✅ Async execution with FastMCP
- ✅ JSON response format
- ✅ Consistent error handling
- ✅ Token-based authentication

### Setup

**1. Install**:
```bash
pip install chora-github
```

**2. Configure Claude Desktop**:
Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "github": {
      "command": "github-mcp",
      "env": {
        "GITHUB_TOKEN": "ghp_your_personal_access_token"
      }
    }
  }
}
```

**3. Restart Claude Desktop**

### MCP Tools

All tools follow this pattern:
- **Input**: Named parameters (owner, repo, etc.)
- **Output**: JSON string with `success` field
- **Authentication**: GitHub PAT via `GITHUB_TOKEN` env var or `token` parameter

---

#### Tool 1: `github:list_issues`

List issues in a GitHub repository.

**Parameters**:
- `owner` (string, required): Repository owner
- `repo` (string, required): Repository name
- `state` (string, optional): Filter by state - "open", "closed", or "all" (default: "open")
- `token` (string, optional): GitHub PAT (uses GITHUB_TOKEN env if not provided)

**Example**:
```python
await list_issues("octocat", "Hello-World", "open")
```

**Response**:
```json
{
  "success": true,
  "data": {
    "issues": [
      {
        "number": 1,
        "title": "Bug in feature X",
        "state": "open",
        "url": "https://github.com/octocat/Hello-World/issues/1",
        "created_at": "2025-01-01T10:00:00Z",
        "updated_at": "2025-01-01T12:00:00Z",
        "body": "Description...",
        "labels": ["bug", "critical"],
        "assignees": ["octocat"],
        "author": "octocat"
      }
    ],
    "total_count": 1
  }
}
```

---

#### Tool 2: `github:create_issue`

Create a new issue in a GitHub repository.

**Parameters**:
- `owner` (string, required): Repository owner
- `repo` (string, required): Repository name
- `title` (string, required): Issue title
- `body` (string, optional): Issue description/body
- `labels` (list[string], optional): List of label names to apply
- `assignees` (list[string], optional): List of usernames to assign
- `token` (string, optional): GitHub PAT

**Example**:
```python
await create_issue(
    "octocat",
    "Hello-World",
    "Found a bug",
    "The feature doesn't work as expected",
    ["bug"],
    ["octocat"]
)
```

**Response**:
```json
{
  "success": true,
  "data": {
    "issue": {
      "number": 42,
      "title": "Found a bug",
      "state": "open",
      "url": "https://github.com/octocat/Hello-World/issues/42",
      "created_at": "2025-01-01T14:30:00Z",
      "labels": ["bug"],
      "assignees": ["octocat"]
    }
  }
}
```

---

#### Tool 3: `github:get_issue`

Get detailed information about a specific issue.

**Parameters**:
- `owner` (string, required): Repository owner
- `repo` (string, required): Repository name
- `issue_number` (int, required): Issue number
- `token` (string, optional): GitHub PAT

**Example**:
```python
await get_issue("octocat", "Hello-World", 1)
```

**Response**: Same format as `list_issues`, but single issue object.

---

#### Tool 4: `github:update_issue`

Update an existing issue (title, body, state, labels, assignees).

**Parameters**:
- `owner` (string, required): Repository owner
- `repo` (string, required): Repository name
- `issue_number` (int, required): Issue number
- `title` (string, optional): New title
- `body` (string, optional): New body/description
- `state` (string, optional): New state ("open" or "closed")
- `labels` (list[string], optional): New labels (replaces existing)
- `assignees` (list[string], optional): New assignees (replaces existing)
- `token` (string, optional): GitHub PAT

**Example**:
```python
await update_issue(
    "octocat",
    "Hello-World",
    1,
    state="closed"
)
```

---

#### Tool 5: `github:list_prs`

List pull requests in a GitHub repository.

**Parameters**:
- `owner` (string, required): Repository owner
- `repo` (string, required): Repository name
- `state` (string, optional): Filter by state - "open", "closed", or "all" (default: "open")
- `head` (string, optional): Filter by head branch
- `base` (string, optional): Filter by base branch
- `page` (int, optional): Page number for pagination (default: 1)
- `per_page` (int, optional): Results per page (default: 30, max: 100)
- `token` (string, optional): GitHub PAT

**Response**:
```json
{
  "success": true,
  "data": {
    "pull_requests": [
      {
        "number": 1,
        "title": "Add new feature",
        "state": "open",
        "url": "https://github.com/octocat/Hello-World/pull/1",
        "created_at": "2025-01-01T10:00:00Z",
        "head_ref": "feature-branch",
        "base_ref": "main",
        "author": "octocat",
        "mergeable": true,
        "merged": false
      }
    ],
    "total_count": 1
  }
}
```

---

#### Tool 6: `github:get_pr`

Get detailed information about a specific pull request.

**Parameters**:
- `owner` (string, required): Repository owner
- `repo` (string, required): Repository name
- `pr_number` (int, required): PR number
- `token` (string, optional): GitHub PAT

**Response**: Same format as `list_prs`, but single PR object.

---

#### Tool 7: `github:get_file_contents`

Get file contents from a GitHub repository.

**Parameters**:
- `owner` (string, required): Repository owner
- `repo` (string, required): Repository name
- `path` (string, required): File path from repository root
- `ref` (string, optional): Branch, tag, or commit SHA (default: repository's default branch)
- `token` (string, optional): GitHub PAT

**Example**:
```python
await get_file_contents("octocat", "Hello-World", "README.md")
```

**Response**:
```json
{
  "success": true,
  "data": {
    "path": "README.md",
    "content": "# Hello World\n\nThis is a test file.",
    "size": 35,
    "encoding": "utf-8",
    "sha": "abc123def456"
  }
}
```

---

#### Tool 8: `github:list_repo_files`

List files in a repository directory.

**Parameters**:
- `owner` (string, required): Repository owner
- `repo` (string, required): Repository name
- `path` (string, optional): Directory path (default: "" for root)
- `ref` (string, optional): Branch, tag, or commit SHA
- `token` (string, optional): GitHub PAT

**Example**:
```python
await list_repo_files("octocat", "Hello-World", "src")
```

**Response**:
```json
{
  "success": true,
  "data": {
    "files": [
      {
        "name": "main.py",
        "path": "src/main.py",
        "type": "file",
        "size": 1024,
        "sha": "def456abc123"
      },
      {
        "name": "utils",
        "path": "src/utils",
        "type": "dir",
        "size": 0,
        "sha": "789ghi012jkl"
      }
    ],
    "path": "src",
    "total_count": 2
  }
}
```

---

### Error Responses

All tools return standardized error responses:

```json
{
  "success": false,
  "error": {
    "type": "GithubNotFoundError",
    "message": "Repository not found"
  }
}
```

**Error Types**:
- `GithubError`: General GitHub API error
- `GithubNotFoundError`: Repository, issue, or PR not found
- `GithubPermissionError`: Insufficient permissions
- `GithubValidationError`: Invalid input data
- `ValueError`: Missing or invalid token

---

### Testing MCP Server

**Run server directly**:
```bash
github-mcp
```

**Test with Claude Desktop**:
1. Configure server in `claude_desktop_config.json`
2. Restart Claude Desktop
3. Use natural language: "List issues in octocat/Hello-World"

---

## See Also

- **[CLI.md](CLI.md)** - CLI reference
- **[AGENTS.md](AGENTS.md)** - Agent awareness guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Architecture documentation

---

**Generated by**: chora-base SAP-047 Capability Server Template
