"""Tests for GitHub tool models (TDD approach)

This test file is written BEFORE implementation to define expected behavior.
Following the chora TDD workflow, these tests will fail initially and drive implementation.
"""


import pytest
from pydantic import ValidationError


class TestListIssuesModels:
    """Test list_issues tool models."""

    def test_list_issues_request_minimal(self):
        """Test list_issues request with minimal required fields."""
        from chora_github.core.models import ListIssuesRequest

        request = ListIssuesRequest(repo="anthropics/anthropic-sdk-python")
        assert request.repo == "anthropics/anthropic-sdk-python"
        assert request.state == "open"  # Default value

    def test_list_issues_request_with_state(self):
        """Test list_issues request with explicit state."""
        from chora_github.core.models import ListIssuesRequest

        request = ListIssuesRequest(repo="owner/repo", state="closed")
        assert request.state == "closed"

    def test_list_issues_request_all_states(self):
        """Test list_issues accepts 'all' state."""
        from chora_github.core.models import ListIssuesRequest

        request = ListIssuesRequest(repo="owner/repo", state="all")
        assert request.state == "all"

    def test_list_issues_request_invalid_state(self):
        """Test list_issues rejects invalid state."""
        from chora_github.core.models import ListIssuesRequest

        with pytest.raises(ValidationError):
            ListIssuesRequest(repo="owner/repo", state="invalid")

    def test_list_issues_response(self):
        """Test list_issues response structure."""
        from chora_github.core.models import IssueData, ListIssuesResponse

        response = ListIssuesResponse(
            issues=[
                IssueData(
                    number=1,
                    title="Test Issue",
                    state="open",
                    url="https://github.com/owner/repo/issues/1",
                    created_at="2025-11-13T00:00:00Z",
                    labels=["bug"],
                )
            ],
            total_count=1,
        )
        assert len(response.issues) == 1
        assert response.total_count == 1
        assert response.issues[0].number == 1
        assert response.issues[0].title == "Test Issue"

    def test_list_issues_response_empty(self):
        """Test list_issues response with no issues."""
        from chora_github.core.models import ListIssuesResponse

        response = ListIssuesResponse(issues=[], total_count=0)
        assert len(response.issues) == 0
        assert response.total_count == 0


class TestCreateIssueModels:
    """Test create_issue tool models."""

    def test_create_issue_request_minimal(self):
        """Test create_issue request with required fields."""
        from chora_github.core.models import CreateIssueRequest

        request = CreateIssueRequest(
            repo="owner/repo", title="Test Issue", body="Test body"
        )
        assert request.repo == "owner/repo"
        assert request.title == "Test Issue"
        assert request.body == "Test body"

    def test_create_issue_request_with_labels(self):
        """Test create_issue with optional labels."""
        from chora_github.core.models import CreateIssueRequest

        request = CreateIssueRequest(
            repo="owner/repo", title="Test", body="Body", labels=["bug", "urgent"]
        )
        assert request.labels == ["bug", "urgent"]

    def test_create_issue_request_with_assignees(self):
        """Test create_issue with optional assignees."""
        from chora_github.core.models import CreateIssueRequest

        request = CreateIssueRequest(
            repo="owner/repo", title="Test", body="Body", assignees=["alice", "bob"]
        )
        assert request.assignees == ["alice", "bob"]

    def test_create_issue_response(self):
        """Test create_issue response."""
        from chora_github.core.models import CreateIssueResponse, IssueData

        response = CreateIssueResponse(
            issue=IssueData(
                number=47,
                title="Test Issue",
                state="open",
                url="https://github.com/owner/repo/issues/47",
                created_at="2025-11-13T00:00:00Z",
            )
        )
        assert response.issue.number == 47
        assert response.issue.state == "open"


class TestGetIssueModels:
    """Test get_issue tool models."""

    def test_get_issue_request(self):
        """Test get_issue request."""
        from chora_github.core.models import GetIssueRequest

        request = GetIssueRequest(repo="owner/repo", issue_number=42)
        assert request.repo == "owner/repo"
        assert request.issue_number == 42

    def test_get_issue_response(self):
        """Test get_issue response."""
        from chora_github.core.models import GetIssueResponse, IssueData

        response = GetIssueResponse(
            issue=IssueData(
                number=42,
                title="Test Issue",
                state="open",
                url="https://github.com/owner/repo/issues/42",
                created_at="2025-11-13T00:00:00Z",
                body="Issue body text",
            )
        )
        assert response.issue.number == 42
        assert response.issue.body == "Issue body text"


class TestUpdateIssueModels:
    """Test update_issue tool models."""

    def test_update_issue_request_title(self):
        """Test update_issue with title change."""
        from chora_github.core.models import UpdateIssueRequest

        request = UpdateIssueRequest(
            repo="owner/repo", issue_number=42, title="New Title"
        )
        assert request.issue_number == 42
        assert request.title == "New Title"

    def test_update_issue_request_state(self):
        """Test update_issue with state change."""
        from chora_github.core.models import UpdateIssueRequest

        request = UpdateIssueRequest(repo="owner/repo", issue_number=42, state="closed")
        assert request.state == "closed"

    def test_update_issue_response(self):
        """Test update_issue response."""
        from chora_github.core.models import IssueData, UpdateIssueResponse

        response = UpdateIssueResponse(
            issue=IssueData(
                number=42,
                title="Updated Title",
                state="closed",
                url="https://github.com/owner/repo/issues/42",
                created_at="2025-11-13T00:00:00Z",
            )
        )
        assert response.issue.title == "Updated Title"
        assert response.issue.state == "closed"


class TestListPRsModels:
    """Test list_prs tool models."""

    def test_list_prs_request(self):
        """Test list_prs request."""
        from chora_github.core.models import ListPRsRequest

        request = ListPRsRequest(repo="owner/repo", state="open")
        assert request.repo == "owner/repo"
        assert request.state == "open"

    def test_list_prs_response(self):
        """Test list_prs response."""
        from chora_github.core.models import ListPRsResponse, PRData

        response = ListPRsResponse(
            pull_requests=[
                PRData(
                    number=10,
                    title="Test PR",
                    state="open",
                    url="https://github.com/owner/repo/pull/10",
                    created_at="2025-11-13T00:00:00Z",
                    head_ref="feature-branch",
                    base_ref="main",
                )
            ],
            total_count=1,
        )
        assert len(response.pull_requests) == 1
        assert response.pull_requests[0].number == 10
        assert response.pull_requests[0].head_ref == "feature-branch"


class TestGetPRModels:
    """Test get_pr tool models."""

    def test_get_pr_request(self):
        """Test get_pr request."""
        from chora_github.core.models import GetPRRequest

        request = GetPRRequest(repo="owner/repo", pr_number=10)
        assert request.repo == "owner/repo"
        assert request.pr_number == 10

    def test_get_pr_response(self):
        """Test get_pr response."""
        from chora_github.core.models import GetPRResponse, PRData

        response = GetPRResponse(
            pull_request=PRData(
                number=10,
                title="Test PR",
                state="open",
                url="https://github.com/owner/repo/pull/10",
                created_at="2025-11-13T00:00:00Z",
                head_ref="feature-branch",
                base_ref="main",
                body="PR description",
            )
        )
        assert response.pull_request.number == 10
        assert response.pull_request.body == "PR description"


class TestGetFileContentsModels:
    """Test get_file_contents tool models."""

    def test_get_file_contents_request(self):
        """Test get_file_contents request."""
        from chora_github.core.models import GetFileContentsRequest

        request = GetFileContentsRequest(
            repo="owner/repo", path="README.md", ref="main"
        )
        assert request.repo == "owner/repo"
        assert request.path == "README.md"
        assert request.ref == "main"

    def test_get_file_contents_request_default_ref(self):
        """Test get_file_contents with default ref."""
        from chora_github.core.models import GetFileContentsRequest

        request = GetFileContentsRequest(repo="owner/repo", path="README.md")
        assert request.ref == "main"  # Default value

    def test_get_file_contents_response(self):
        """Test get_file_contents response."""
        from chora_github.core.models import GetFileContentsResponse

        response = GetFileContentsResponse(
            path="README.md",
            content="# Test Repository\n\nThis is a test.",
            size=35,
            encoding="utf-8",
        )
        assert response.path == "README.md"
        assert "Test Repository" in response.content
        assert response.size == 35


class TestListRepoFilesModels:
    """Test list_repo_files tool models."""

    def test_list_repo_files_request(self):
        """Test list_repo_files request."""
        from chora_github.core.models import ListRepoFilesRequest

        request = ListRepoFilesRequest(repo="owner/repo", path="src", ref="main")
        assert request.repo == "owner/repo"
        assert request.path == "src"
        assert request.ref == "main"

    def test_list_repo_files_request_root(self):
        """Test list_repo_files at root."""
        from chora_github.core.models import ListRepoFilesRequest

        request = ListRepoFilesRequest(repo="owner/repo")
        assert request.path == ""  # Default to root
        assert request.ref == "main"

    def test_list_repo_files_response(self):
        """Test list_repo_files response."""
        from chora_github.core.models import FileData, ListRepoFilesResponse

        response = ListRepoFilesResponse(
            files=[
                FileData(name="README.md", path="README.md", type="file", size=1024),
                FileData(name="src", path="src", type="dir", size=0),
            ],
            total_count=2,
        )
        assert len(response.files) == 2
        assert response.files[0].type == "file"
        assert response.files[1].type == "dir"


class TestToolMetadata:
    """Test tool definition metadata models."""

    def test_tool_definition_structure(self):
        """Test ToolDefinition model."""
        from chora_github.core.models import ToolDefinition, ToolParameter

        tool = ToolDefinition(
            name="list_issues",
            description="List issues in a repository",
            parameters=[
                ToolParameter(
                    name="repo",
                    type="string",
                    description="Repository in owner/repo format",
                    required=True,
                ),
                ToolParameter(
                    name="state",
                    type="string",
                    description="Issue state filter",
                    required=False,
                    enum=["open", "closed", "all"],
                ),
            ],
        )
        assert tool.name == "list_issues"
        assert len(tool.parameters) == 2
        assert tool.parameters[0].required is True
        assert tool.parameters[1].enum == ["open", "closed", "all"]

    def test_tool_parameter_with_default(self):
        """Test ToolParameter with default value."""
        from chora_github.core.models import ToolParameter

        param = ToolParameter(
            name="state",
            type="string",
            description="Issue state",
            required=False,
            default="open",
        )
        assert param.default == "open"
        assert param.required is False


class TestToolCallEnvelope:
    """Test tool call request/response envelope."""

    def test_tool_call_request(self):
        """Test ToolCallRequest envelope."""
        from chora_github.core.models import ToolCallRequest

        request = ToolCallRequest(
            tool="list_issues", parameters={"repo": "owner/repo", "state": "open"}
        )
        assert request.tool == "list_issues"
        assert request.parameters["repo"] == "owner/repo"

    def test_tool_call_response_success(self):
        """Test successful ToolCallResponse."""
        from chora_github.core.models import ToolCallResponse

        response = ToolCallResponse(
            success=True, result={"issues": [], "total_count": 0}
        )
        assert response.success is True
        assert response.error is None

    def test_tool_call_response_error(self):
        """Test error ToolCallResponse."""
        from chora_github.core.models import ToolCallResponse

        response = ToolCallResponse(
            success=False, error="Repository not found", error_code="NOT_FOUND"
        )
        assert response.success is False
        assert response.error == "Repository not found"
        assert response.error_code == "NOT_FOUND"

    def test_tool_call_response_partial_success(self):
        """Test ToolCallResponse with warning."""
        from chora_github.core.models import ToolCallResponse

        response = ToolCallResponse(
            success=True,
            result={"issues": [], "total_count": 0},
            warning="API rate limit approaching",
        )
        assert response.success is True
        assert response.warning is not None


class TestCommonDataModels:
    """Test common data models used across tools."""

    def test_issue_data_minimal(self):
        """Test IssueData with minimal fields."""
        from chora_github.core.models import IssueData

        issue = IssueData(
            number=1,
            title="Test",
            state="open",
            url="https://github.com/owner/repo/issues/1",
            created_at="2025-11-13T00:00:00Z",
        )
        assert issue.number == 1
        assert issue.state == "open"

    def test_issue_data_full(self):
        """Test IssueData with all fields."""
        from chora_github.core.models import IssueData

        issue = IssueData(
            number=1,
            title="Test Issue",
            state="open",
            url="https://github.com/owner/repo/issues/1",
            created_at="2025-11-13T00:00:00Z",
            updated_at="2025-11-13T01:00:00Z",
            body="Issue body",
            labels=["bug", "urgent"],
            assignees=["alice"],
            author="bob",
        )
        assert issue.body == "Issue body"
        assert len(issue.labels) == 2
        assert issue.assignees == ["alice"]

    def test_pr_data(self):
        """Test PRData model."""
        from chora_github.core.models import PRData

        pr = PRData(
            number=10,
            title="Test PR",
            state="open",
            url="https://github.com/owner/repo/pull/10",
            created_at="2025-11-13T00:00:00Z",
            head_ref="feature",
            base_ref="main",
        )
        assert pr.number == 10
        assert pr.head_ref == "feature"
        assert pr.base_ref == "main"

    def test_file_data(self):
        """Test FileData model."""
        from chora_github.core.models import FileData

        file = FileData(name="README.md", path="README.md", type="file", size=1024)
        assert file.name == "README.md"
        assert file.type == "file"
        assert file.size == 1024
