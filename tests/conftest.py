"""Test Configuration and Fixtures

Shared fixtures for testing GitHub capability server across all interfaces.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List
from unittest.mock import Mock, AsyncMock

import pytest

from chora_github.core.models import (
    IssueData,
    PRData,
    FileData,
    ListIssuesResponse,
    CreateIssueResponse,
    GetIssueResponse,
    UpdateIssueResponse,
    ListPRsResponse,
    GetPRResponse,
    GetFileContentsResponse,
    ListRepoFilesResponse,
)


# ============================================================================
# Sample Data Fixtures
# ============================================================================


@pytest.fixture
def sample_issue_data() -> Dict[str, Any]:
    """Sample issue data matching GitHub API format."""
    return {
        "number": 1,
        "title": "Test Issue",
        "body": "This is a test issue",
        "state": "open",
        "url": "https://github.com/octocat/Hello-World/issues/1",
        "created_at": "2025-11-01T10:00:00Z",
        "updated_at": "2025-11-01T12:00:00Z",
        "labels": ["bug", "enhancement"],
        "assignees": ["octocat"],
        "author": "octocat",
    }


@pytest.fixture
def sample_pr_data() -> Dict[str, Any]:
    """Sample PR data matching GitHub API format."""
    return {
        "number": 1,
        "title": "Test Pull Request",
        "body": "This is a test PR",
        "state": "open",
        "url": "https://github.com/octocat/Hello-World/pull/1",
        "created_at": "2025-11-01T10:00:00Z",
        "updated_at": "2025-11-01T12:00:00Z",
        "head_ref": "feature-branch",
        "base_ref": "main",
        "author": "octocat",
        "mergeable": True,
        "merged": False,
    }


@pytest.fixture
def sample_file_data() -> Dict[str, Any]:
    """Sample file data matching GitHub API format."""
    return {
        "name": "README.md",
        "path": "README.md",
        "type": "file",
        "size": 1024,
        "sha": "abc123def456",
    }


# ============================================================================
# Model Fixtures
# ============================================================================


@pytest.fixture
def issue(sample_issue_data) -> IssueData:
    """Create IssueData model instance."""
    return IssueData(**sample_issue_data)


@pytest.fixture
def pr(sample_pr_data) -> PRData:
    """Create PRData model instance."""
    return PRData(**sample_pr_data)


@pytest.fixture
def file_data(sample_file_data) -> FileData:
    """Create FileData model instance."""
    return FileData(**sample_file_data)


# ============================================================================
# Mock GithubToolService Fixtures
# ============================================================================


@pytest.fixture
def mock_github_service(issue, pr, file_data):
    """Create mock GithubToolService with predefined responses."""
    service = Mock()

    # Mock list_issues
    service.list_issues.return_value = ListIssuesResponse(
        issues=[issue],
        total_count=1,
    )

    # Mock create_issue
    service.create_issue.return_value = CreateIssueResponse(
        issue=issue,
    )

    # Mock get_issue
    def get_issue_side_effect(request):
        from chora_github.core.exceptions import GithubNotFoundError
        if request.issue_number == 1:
            return GetIssueResponse(issue=issue)
        raise GithubNotFoundError(f"Issue #{request.issue_number} not found")

    service.get_issue.side_effect = get_issue_side_effect

    # Mock update_issue
    updated_issue_data = issue.model_copy(deep=True)
    updated_issue_data.title = "Updated Issue"
    service.update_issue.return_value = UpdateIssueResponse(
        issue=updated_issue_data,
    )

    # Mock list_prs
    service.list_prs.return_value = ListPRsResponse(
        pull_requests=[pr],
        total_count=1,
    )

    # Mock get_pr
    def get_pr_side_effect(request):
        from chora_github.core.exceptions import GithubNotFoundError
        if request.pr_number == 1:
            return GetPRResponse(pr=pr)
        raise GithubNotFoundError(f"PR #{request.pr_number} not found")

    service.get_pr.side_effect = get_pr_side_effect

    # Mock get_file_contents
    service.get_file_contents.return_value = GetFileContentsResponse(
        content="# Hello World\n\nThis is a test file.",
        encoding="utf-8",
        size=35,
        path="README.md",
        sha="abc123def456",
    )

    # Mock list_repo_files
    service.list_repo_files.return_value = ListRepoFilesResponse(
        files=[file_data],
        path="",
        total_count=1,
    )

    return service


# ============================================================================
# MCP Test Fixtures
# ============================================================================


@pytest.fixture
def mcp_tool_executor(mock_github_service):
    """Create MCP tool executor with mocked service.

    This fixture provides access to all MCP tool implementations
    by patching the _get_service function to return mock service.
    """
    from unittest.mock import patch

    # Patch _get_service to return our mock
    with patch('chora_github.interfaces.mcp.tools._get_service', return_value=mock_github_service):
        # Import tools module to get access to tool functions
        from chora_github.interfaces.mcp import tools
        yield tools


@pytest.fixture
def mcp_resource_executor(mock_github_service):
    """Create MCP resource executor with mocked service.

    This fixture provides access to all MCP resource implementations
    by patching the _get_service function to return mock service.
    """
    from unittest.mock import patch

    # Patch _get_service to return our mock
    with patch('chora_github.interfaces.mcp.resources._get_service', return_value=mock_github_service):
        # Import resources module to get access to resource functions
        from chora_github.interfaces.mcp import resources
        yield resources


# ============================================================================
# Helper Fixtures
# ============================================================================


@pytest.fixture
def multiple_issues(sample_issue_data) -> List[IssueData]:
    """Create multiple issue instances for testing."""
    issues = []
    for i in range(5):
        data = sample_issue_data.copy()
        data["number"] = i + 1
        data["title"] = f"Test Issue {i + 1}"
        data["state"] = "open" if i % 2 == 0 else "closed"
        data["labels"] = ["bug"] if i < 3 else []
        issues.append(IssueData(**data))
    return issues


@pytest.fixture
def multiple_prs(sample_pr_data) -> List[PRData]:
    """Create multiple PR instances for testing."""
    prs = []
    for i in range(3):
        data = sample_pr_data.copy()
        data["number"] = i + 1
        data["title"] = f"Test PR {i + 1}"
        data["state"] = "open" if i % 2 == 0 else "closed"
        prs.append(PRData(**data))
    return prs


@pytest.fixture
def multiple_files(sample_file_data) -> List[FileData]:
    """Create multiple file instances for testing."""
    files = []
    file_names = ["README.md", "setup.py", "requirements.txt", ".gitignore"]
    for i, name in enumerate(file_names):
        data = sample_file_data.copy()
        data["name"] = name
        data["path"] = name
        data["type"] = "file"
        files.append(FileData(**data))
    return files
