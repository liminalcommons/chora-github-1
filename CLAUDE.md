---
title: GitHub - Claude Agent Awareness
type: reference
status: active
last_updated: '2025-11-19'
tags:
- documentation
- reference
---

# GitHub - Claude Agent Awareness

**Generated from**: chora-base 5.0.0 (SAP-047 Capability Server Template)
**Project**: github
**Namespace**: github
**Architecture**: Capability Server with CLI + REST + MCP interfaces

---

## ⚠️ CRITICAL: Read This First!

This project was generated from **chora-base 5.0.0** using the **SAP-047 Capability Server Template** generator. It follows the capability server architecture pattern with:

- **Core/Interface Separation** (SAP-042): Business logic isolated from interface implementations
- **Multi-Interface Support** (SAP-043): CLI, REST API, and MCP (Model Context Protocol)







---

## Quick Start for Claude Code

### First-Time Setup

1. **Read this file** (CLAUDE.md) for project overview and navigation
2. **Read [VERIFICATION.md](VERIFICATION.md)** for verification workflow (if verifying)
3. **Read [README.md](README.md)** for user-facing documentation
4. **Read architecture documentation** in `docs/architecture/` for deep understanding

### Verification Workflow

**If you are verifying this project**:
1. Follow [VERIFICATION.md](VERIFICATION.md) for L1-L4 verification steps
2. See comprehensive plan: [PLAN-2025-11-12-SAP-047-PHASE-6-L4-VERIFICATION.md](https://github.com/liminalcommons/chora-base/blob/main/docs/project-docs/plans/PLAN-2025-11-12-SAP-047-PHASE-6-L4-VERIFICATION.md)
3. Document results in `.chora/verification/` directory

### Development Workflow

**If you are developing new features**:
1. Core business logic goes in `github/core/`
2. Interface implementations go in `github/interfaces/`
3. Infrastructure patterns go in `github/infrastructure/`
4. Tests go in `tests/` (mirror the package structure)
5. Follow TDD: write tests first, then implementation

---

## Architecture Overview

### Project Structure

```
github/
├── core/                          # Business logic (interface-agnostic)
│   ├── models.py                  # Domain models (Pydantic)
│   ├── service.py                 # Core service implementation
│   └── interface.py               # Abstract interface definition
│
├── interfaces/                    # Interface implementations
│   ├── cli/                       # CLI interface (Click)
│   │   └── commands.py
│   ├── rest/                      # REST API interface (FastAPI)
│   │   └── app.py
│   ├── mcp/                       # MCP interface (FastMCP)
│   │   ├── __init__.py           # Server setup
│   │   ├── tools.py              # MCP tool implementations
│   │   └── resources.py          # MCP resource implementations
│
├── tests/                         # Test suite (mirrors package)
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   └── conftest.py                # Pytest fixtures
│
├── docs/                          # Documentation
│   ├── architecture/              # Architecture docs
│   ├── api/                       # API reference
│   └── guides/                    # User guides
│
├── Dockerfile                     # Multi-stage Docker build
├── pyproject.toml                 # Python package configuration
└── README.md                      # User-facing documentation
```

---

## Capability Server Architecture (SAP-042)

### Core/Interface Separation

**Core Layer** (`github/core/`):
- **Purpose**: Business logic, domain models, service implementation
- **Dependencies**: Pure Python, Pydantic, domain-specific libraries
- **No dependencies on**: Click, FastAPI, FastMCP, or any interface libraries
- **Testing**: Unit tests with fast execution

**Interface Layer** (`github/interfaces/`):
- **Purpose**: Expose core functionality via CLI, REST, and MCP
- **Dependencies**: Click (CLI), FastAPI (REST), FastMCP (MCP)
- **Pattern**: Each interface imports core and adapts to its protocol
- **Testing**: Integration tests verifying interface contracts

**Benefits**:
- 80% reduction in coupling
- Easy to add new interfaces
- Fast unit testing (no interface overhead)
- Clear separation of concerns

---

## Multi-Interface Support (SAP-043)

This project provides 3 interfaces to the same core capability:

### 1. CLI Interface (Click)
```bash
# Installation
pip install github

# Usage
github --help
github health
```

**When to use**: Command-line scripting, automation, CI/CD pipelines

---

### 2. REST API Interface (FastAPI)
```bash
# Start server
uvicorn github.interfaces.rest.app:app --host 0.0.0.0 --port 8000

# Usage
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Swagger UI
```

**When to use**: HTTP clients, web applications, microservices integration

---

### 3. MCP Interface (Model Context Protocol)

**Entry point**: `github-mcp`

**Setup for Claude Desktop**:

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

**Available Tools** (8 total):
- `github:list_issues` - List issues in a repository
- `github:create_issue` - Create a new issue
- `github:get_issue` - Get issue details by number
- `github:update_issue` - Update existing issue
- `github:list_prs` - List pull requests in a repository
- `github:get_pr` - Get pull request details by number
- `github:get_file_contents` - Get file contents from repository
- `github:list_repo_files` - List files in repository directory

**Usage Examples** (natural language in Claude Desktop):
```
"List open issues in octocat/Hello-World"
"Create an issue titled 'Bug fix' in my-org/my-repo"
"Show me the README.md from octocat/Hello-World"
"List pull requests in my-org/my-repo with state open"
"Get issue #42 from octocat/Hello-World"
```

**When to use**: AI assistants (Claude Desktop), conversational interfaces, agent-driven workflows

---

**All interfaces share the same core service**, ensuring consistency across CLI, REST, and MCP.

---





## Development Guidelines

### 1. Core Business Logic

**All business logic goes in `github/core/`**:
- Models: Pydantic models in `core/models.py`
- Service: Business logic in `core/service.py`
- Interface: Abstract interface in `core/interface.py`

**Example**:
```python
# github/core/models.py
from pydantic import BaseModel

class CapabilityRequest(BaseModel):
    """Request model for capability execution."""
    input: str

class CapabilityResponse(BaseModel):
    """Response model for capability execution."""
    output: str

# github/core/service.py
from .models import CapabilityRequest, CapabilityResponse
from .interface import AbstractCapabilityService

class CapabilityService(AbstractCapabilityService):
    """Core business logic (interface-agnostic)."""

    def execute(self, request: CapabilityRequest) -> CapabilityResponse:
        # Business logic here
        return CapabilityResponse(output=f"Processed: {request.input}")
```

---

### 2. Interface Implementations

**Each interface adapts core to its protocol**:

**CLI** (`github/interfaces/cli/commands.py`):
```python
import click
from github.core.service import CapabilityService
from github.core.models import CapabilityRequest

@click.command()
@click.argument("input")
def execute(input: str):
    """Execute capability via CLI."""
    service = CapabilityService()
    request = CapabilityRequest(input=input)
    response = service.execute(request)
    click.echo(response.output)
```

**REST** (`github/interfaces/rest/app.py`):
```python
from fastapi import FastAPI
from github.core.service import CapabilityService
from github.core.models import CapabilityRequest, CapabilityResponse

app = FastAPI()
service = CapabilityService()

@app.post("/execute")
def execute(request: CapabilityRequest) -> CapabilityResponse:
    """Execute capability via REST API."""
    return service.execute(request)
```


---

### 3. Testing Strategy

**Unit Tests** (`tests/unit/`):
- Test core business logic in isolation
- Fast execution (<5s for all unit tests)
- No interface dependencies

**Integration Tests** (`tests/integration/`):
- Test interface implementations
- Verify CLI commands, REST endpoints
- Slower execution (database, network, etc.)

**Coverage Target**: ≥85%

---

### 4. Quality Gates

**Pre-commit hooks** (automated):
```bash
# Ruff linting
ruff check .

# Ruff formatting
ruff format .

# Mypy type checking
mypy github
```

**Run manually**:
```bash
# All quality gates
pre-commit run --all-files

# Tests
pytest

# Coverage
pytest --cov=github --cov-report=term-missing
```

---

### 5. Docker Deployment

**Build**:
```bash
docker build -t github:latest .
```

**Run CLI**:
```bash
docker run --rm github:latest github --help
```

**Run REST API**:
```bash
docker run -d -p 8000:8000 github:latest
curl http://localhost:8000/health
```

---

## Verification Workflow

**If you are Claude Code verifying this project**, see [VERIFICATION.md](VERIFICATION.md) for:
- L1-L4 verification checklists
- Command snippets for each verification level
- Report templates
- Success criteria

**Comprehensive Plan**: [PLAN-2025-11-12-SAP-047-PHASE-6-L4-VERIFICATION.md](https://github.com/liminalcommons/chora-base/blob/main/docs/project-docs/plans/PLAN-2025-11-12-SAP-047-PHASE-6-L4-VERIFICATION.md)

---

## Common Tasks for Claude Code

### Task: Add New CLI Command

1. Define in `github/interfaces/cli/commands.py`:
```python
@click.command()
def my_command():
    """My new command."""
    click.echo("Hello!")
```

2. Add to CLI group in same file
3. Test: `github my-command`
4. Add test in `tests/integration/test_cli.py`

---

### Task: Add New REST Endpoint

1. Define in `github/interfaces/rest/app.py`:
```python
@app.get("/my-endpoint")
def my_endpoint():
    """My new endpoint."""
    return {"message": "Hello!"}
```

2. Test: `curl http://localhost:8000/my-endpoint`
3. Add test in `tests/integration/test_rest.py`

---

### Task: Add New MCP Tool

1. Define in `github/interfaces/mcp/tools.py`:
```python
@mcp.tool()
async def github_my_tool(
    param: str = Field(..., description="Parameter description")
) -> str:
    """My new MCP tool description."""
    service = _get_service()
    # Use core service here
    return "Result"
```

2. Register in `register_tools()` function (already done via decorator)
3. Test in Claude Desktop or with MCP client
4. Add test in `tests/interfaces/test_mcp.py`
5. Document in `API.md` MCP section

---

### Task: Add Core Business Logic

1. Define models in `github/core/models.py`
2. Implement logic in `github/core/service.py`
3. Update abstract interface in `github/core/interface.py`
4. Adapt all interfaces (CLI, REST) to use new logic
5. Add unit tests in `tests/unit/test_service.py`

---

### Task: Add New Feature Flag

1. Add to `pyproject.toml` optional dependencies
2. Add conditional import in relevant module
3. Document in README.md
4. Add test coverage for both enabled/disabled states

---

## Related Documentation

### In This Repository
- [README.md](README.md) - User-facing documentation
- [VERIFICATION.md](VERIFICATION.md) - Verification workflow (L1-L4)
- [docs/architecture/](docs/architecture/) - Architecture documentation
- [docs/api/](docs/api/) - API reference
- [docs/guides/](docs/guides/) - User guides

### In chora-base Repository
- **Comprehensive Verification Plan**: [PLAN-2025-11-12-SAP-047-PHASE-6-L4-VERIFICATION.md](https://github.com/liminalcommons/chora-base/blob/main/docs/project-docs/plans/PLAN-2025-11-12-SAP-047-PHASE-6-L4-VERIFICATION.md)
- **chora-base**: [https://github.com/liminalcommons/chora-base](https://github.com/liminalcommons/chora-base)
- **SAP-042 (Interface Design)**: [docs/skilled-awareness/interface-design/](https://github.com/liminalcommons/chora-base/tree/main/docs/skilled-awareness/interface-design)
- **SAP-043 (Multi-Interface)**: [docs/skilled-awareness/multi-interface/](https://github.com/liminalcommons/chora-base/tree/main/docs/skilled-awareness/multi-interface)



- **SAP-047 (Capability Server Template)**: [docs/skilled-awareness/capability-server-template/](https://github.com/liminalcommons/chora-base/tree/main/docs/skilled-awareness/capability-server-template)

---

## Support and Issues

**Found a bug or have a question?**
1. Check existing issues: [https://github.com/liminalcommons/github/issues](https://github.com/liminalcommons/github/issues)
2. Create new issue if not found

**Generator issues?**
- Report in chora-base: [https://github.com/liminalcommons/chora-base/issues](https://github.com/liminalcommons/chora-base/issues)
- Tag with `SAP-047`

---

## Version History

- **1.1.0** (2025-11-19): MCP Interface Addition
  - Added MCP (Model Context Protocol) interface
  - 8 MCP tools for GitHub operations (issues, PRs, files)
  - Comprehensive test suite (30 tests for MCP)
  - Updated documentation for 3-interface pattern

- **1.0.0** (Initial Release): Generated from chora-base 5.0.0
  - Capability server architecture (SAP-042-047)
  - CLI + REST interfaces







---

**Generated by**: chora-base 5.0.0 SAP-047 Capability Server Template
**Last Updated**: {{ timestamp }}
