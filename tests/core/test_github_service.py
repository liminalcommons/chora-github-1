"""Tests for GitHub service layer (TDD approach)

This test file is written BEFORE implementation to define expected behavior.
The service layer integrates with PyGithub to implement the 8 GitHub tools.
"""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest


class TestGithubServiceInitialization:
    """Test GitHub service initialization."""

    def test_service_requires_token(self):
        """Test that service initialization requires a GitHub token."""
        from chora_github.core.services import GithubToolService

        # Should raise error if no token provided
        with pytest.raises(ValueError, match="GitHub token is required"):
            GithubToolService(token=None)

        with pytest.raises(ValueError, match="GitHub token is required"):
            GithubToolService(token="")

    def test_service_initializes_with_token(self):
        """Test successful service initialization with token."""
        from chora_github.core.services import GithubToolService

        service = GithubToolService(token="ghp_test_token_12345")
        assert service is not None
        assert service.token == "ghp_test_token_12345"


class TestListIssuesTool:
    """Test list_issues tool implementation."""

    @pytest.fixture
    def mock_github(self):
        """Mock PyGithub client."""
        with patch("chora_github.core.services.Github") as mock:
            yield mock

    @pytest.fixture
    def service(self, mock_github):
        """Create service instance with mocked Github client."""
        from chora_github.core.services import GithubToolService

        return GithubToolService(token="ghp_test_token")

    def test_list_issues_success(self, service, mock_github):
        """Test successful list_issues call."""
        from chora_github.core.models import IssueState, ListIssuesRequest

        # Mock GitHub API response
        mock_repo = Mock()
        mock_issue = Mock()
        mock_issue.number = 1
        mock_issue.title = "Test Issue"
        mock_issue.state = "open"
        mock_issue.html_url = "https://github.com/owner/repo/issues/1"
        mock_issue.created_at = datetime(2025, 11, 13)
        mock_issue.updated_at = datetime(2025, 11, 13)
        mock_issue.body = "Test body"
        mock_issue.labels = []
        mock_issue.assignees = []
        mock_issue.user.login = "testuser"

        mock_repo.get_issues.return_value = [mock_issue]
        mock_github.return_value.get_repo.return_value = mock_repo

        # Execute
        request = ListIssuesRequest(repo="owner/repo", state=IssueState.OPEN)
        response = service.list_issues(request)

        # Verify
        assert response.total_count == 1
        assert len(response.issues) == 1
        assert response.issues[0].number == 1
        assert response.issues[0].title == "Test Issue"

    def test_list_issues_repository_not_found(self, service, mock_github):
        """Test list_issues with non-existent repository."""
        from github import UnknownObjectException

        from chora_github.core.exceptions import GithubNotFoundError
        from chora_github.core.models import ListIssuesRequest

        # Mock GitHub API error
        mock_github.return_value.get_repo.side_effect = UnknownObjectException(
            404, "Not Found"
        )

        # Execute
        request = ListIssuesRequest(repo="nonexistent/repo")

        # Verify
        with pytest.raises(GithubNotFoundError):
            service.list_issues(request)

    def test_list_issues_with_filters(self, service, mock_github):
        """Test list_issues with label and assignee filters."""
        from chora_github.core.models import ListIssuesRequest

        # Mock
        mock_repo = Mock()
        mock_repo.get_issues.return_value = []
        mock_github.return_value.get_repo.return_value = mock_repo

        # Execute
        request = ListIssuesRequest(repo="owner/repo", labels=["bug"], assignee="alice")
        response = service.list_issues(request)

        # Verify get_issues was called with correct filters
        mock_repo.get_issues.assert_called_once()
        assert response.total_count == 0


class TestCreateIssueTool:
    """Test create_issue tool implementation."""

    @pytest.fixture
    def mock_github(self):
        """Mock PyGithub client."""
        with patch("chora_github.core.services.Github") as mock:
            yield mock

    @pytest.fixture
    def service(self, mock_github):
        """Create service instance with mocked Github client."""
        from chora_github.core.services import GithubToolService

        return GithubToolService(token="ghp_test_token")

    def test_create_issue_success(self, service, mock_github):
        """Test successful issue creation."""
        from chora_github.core.models import CreateIssueRequest

        # Mock
        mock_repo = Mock()
        mock_issue = Mock()
        mock_issue.number = 47
        mock_issue.title = "Test Issue"
        mock_issue.state = "open"
        mock_issue.html_url = "https://github.com/owner/repo/issues/47"
        mock_issue.created_at = datetime(2025, 11, 13)
        mock_issue.updated_at = None
        mock_issue.body = "Test body"
        mock_issue.labels = []
        mock_issue.assignees = []
        mock_issue.user.login = "testuser"

        mock_repo.create_issue.return_value = mock_issue
        mock_github.return_value.get_repo.return_value = mock_repo

        # Execute
        request = CreateIssueRequest(
            repo="owner/repo", title="Test Issue", body="Test body"
        )
        response = service.create_issue(request)

        # Verify
        assert response.issue.number == 47
        assert response.issue.title == "Test Issue"
        mock_repo.create_issue.assert_called_once_with(
            title="Test Issue", body="Test body", labels=None, assignees=None
        )

    def test_create_issue_with_labels_and_assignees(self, service, mock_github):
        """Test issue creation with labels and assignees."""
        from chora_github.core.models import CreateIssueRequest

        # Mock
        mock_repo = Mock()
        mock_issue = Mock()
        mock_issue.number = 48
        mock_issue.title = "Test"
        mock_issue.state = "open"
        mock_issue.html_url = "https://github.com/owner/repo/issues/48"
        mock_issue.created_at = datetime(2025, 11, 13)
        mock_issue.updated_at = datetime(2025, 11, 13)
        mock_issue.body = "Body"

        # Mock labels with name attribute
        mock_label1 = Mock()
        mock_label1.name = "bug"
        mock_label2 = Mock()
        mock_label2.name = "urgent"
        mock_issue.labels = [mock_label1, mock_label2]

        # Mock assignees with login attribute
        mock_assignee = Mock()
        mock_assignee.login = "alice"
        mock_issue.assignees = [mock_assignee]

        mock_issue.user.login = "testuser"

        mock_repo.create_issue.return_value = mock_issue
        mock_github.return_value.get_repo.return_value = mock_repo

        # Execute
        request = CreateIssueRequest(
            repo="owner/repo",
            title="Test",
            body="Body",
            labels=["bug", "urgent"],
            assignees=["alice"],
        )
        response = service.create_issue(request)

        # Verify
        assert len(response.issue.labels) == 2
        assert len(response.issue.assignees) == 1


class TestGetIssueTool:
    """Test get_issue tool implementation."""

    @pytest.fixture
    def mock_github(self):
        """Mock PyGithub client."""
        with patch("chora_github.core.services.Github") as mock:
            yield mock

    @pytest.fixture
    def service(self, mock_github):
        """Create service instance with mocked Github client."""
        from chora_github.core.services import GithubToolService

        return GithubToolService(token="ghp_test_token")

    def test_get_issue_success(self, service, mock_github):
        """Test successful get_issue call."""
        from chora_github.core.models import GetIssueRequest

        # Mock
        mock_repo = Mock()
        mock_issue = Mock()
        mock_issue.number = 42
        mock_issue.title = "Test Issue"
        mock_issue.state = "open"
        mock_issue.html_url = "https://github.com/owner/repo/issues/42"
        mock_issue.created_at = datetime(2025, 11, 13)
        mock_issue.updated_at = datetime(2025, 11, 13)
        mock_issue.body = "Detailed description"
        mock_issue.labels = []
        mock_issue.assignees = []
        mock_issue.user.login = "testuser"

        mock_repo.get_issue.return_value = mock_issue
        mock_github.return_value.get_repo.return_value = mock_repo

        # Execute
        request = GetIssueRequest(repo="owner/repo", issue_number=42)
        response = service.get_issue(request)

        # Verify
        assert response.issue.number == 42
        assert response.issue.body == "Detailed description"
        mock_repo.get_issue.assert_called_once_with(42)


class TestUpdateIssueTool:
    """Test update_issue tool implementation."""

    @pytest.fixture
    def mock_github(self):
        """Mock PyGithub client."""
        with patch("chora_github.core.services.Github") as mock:
            yield mock

    @pytest.fixture
    def service(self, mock_github):
        """Create service instance with mocked Github client."""
        from chora_github.core.services import GithubToolService

        return GithubToolService(token="ghp_test_token")

    def test_update_issue_title(self, service, mock_github):
        """Test updating issue title."""
        from chora_github.core.models import UpdateIssueRequest

        # Mock
        mock_repo = Mock()
        mock_issue = Mock()
        mock_issue.number = 42
        mock_issue.title = "Updated Title"
        mock_issue.state = "open"
        mock_issue.html_url = "https://github.com/owner/repo/issues/42"
        mock_issue.created_at = datetime(2025, 11, 13)
        mock_issue.updated_at = datetime(2025, 11, 13)
        mock_issue.body = "Original body"
        mock_issue.labels = []
        mock_issue.assignees = []
        mock_issue.user.login = "testuser"

        mock_issue.edit.return_value = None  # edit() modifies in place
        mock_repo.get_issue.return_value = mock_issue
        mock_github.return_value.get_repo.return_value = mock_repo

        # Execute
        request = UpdateIssueRequest(
            repo="owner/repo", issue_number=42, title="Updated Title"
        )
        response = service.update_issue(request)

        # Verify
        assert response.issue.title == "Updated Title"
        mock_issue.edit.assert_called_once()

    def test_update_issue_state(self, service, mock_github):
        """Test updating issue state to closed."""
        from chora_github.core.models import IssueState, UpdateIssueRequest

        # Mock
        mock_repo = Mock()
        mock_issue = Mock()
        mock_issue.number = 42
        mock_issue.state = "closed"
        mock_issue.html_url = "https://github.com/owner/repo/issues/42"
        mock_issue.created_at = datetime(2025, 11, 13)
        mock_issue.updated_at = datetime(2025, 11, 13)
        mock_issue.title = "Test Issue"
        mock_issue.body = "Original body"
        mock_issue.labels = []
        mock_issue.assignees = []
        mock_issue.user.login = "testuser"

        mock_issue.edit.return_value = None
        mock_repo.get_issue.return_value = mock_issue
        mock_github.return_value.get_repo.return_value = mock_repo

        # Execute
        request = UpdateIssueRequest(
            repo="owner/repo", issue_number=42, state=IssueState.CLOSED
        )
        response = service.update_issue(request)

        # Verify
        assert response.issue.state == "closed"


class TestListPRsTool:
    """Test list_prs tool implementation."""

    @pytest.fixture
    def mock_github(self):
        """Mock PyGithub client."""
        with patch("chora_github.core.services.Github") as mock:
            yield mock

    @pytest.fixture
    def service(self, mock_github):
        """Create service instance with mocked Github client."""
        from chora_github.core.services import GithubToolService

        return GithubToolService(token="ghp_test_token")

    def test_list_prs_success(self, service, mock_github):
        """Test successful list_prs call."""
        from chora_github.core.models import ListPRsRequest

        # Mock
        mock_repo = Mock()
        mock_pr = Mock()
        mock_pr.number = 10
        mock_pr.title = "Test PR"
        mock_pr.state = "open"
        mock_pr.html_url = "https://github.com/owner/repo/pull/10"
        mock_pr.created_at = datetime(2025, 11, 13)
        mock_pr.updated_at = datetime(2025, 11, 13)
        mock_pr.head.ref = "feature-branch"
        mock_pr.base.ref = "main"
        mock_pr.body = "PR description"
        mock_pr.user.login = "testuser"
        mock_pr.mergeable = True
        mock_pr.merged = False

        mock_repo.get_pulls.return_value = [mock_pr]
        mock_github.return_value.get_repo.return_value = mock_repo

        # Execute
        request = ListPRsRequest(repo="owner/repo")
        response = service.list_prs(request)

        # Verify
        assert response.total_count == 1
        assert response.pull_requests[0].number == 10
        assert response.pull_requests[0].head_ref == "feature-branch"


class TestGetPRTool:
    """Test get_pr tool implementation."""

    @pytest.fixture
    def mock_github(self):
        """Mock PyGithub client."""
        with patch("chora_github.core.services.Github") as mock:
            yield mock

    @pytest.fixture
    def service(self, mock_github):
        """Create service instance with mocked Github client."""
        from chora_github.core.services import GithubToolService

        return GithubToolService(token="ghp_test_token")

    def test_get_pr_success(self, service, mock_github):
        """Test successful get_pr call."""
        from chora_github.core.models import GetPRRequest

        # Mock
        mock_repo = Mock()
        mock_pr = Mock()
        mock_pr.number = 10
        mock_pr.title = "Test PR"
        mock_pr.state = "open"
        mock_pr.html_url = "https://github.com/owner/repo/pull/10"
        mock_pr.created_at = datetime(2025, 11, 13)
        mock_pr.updated_at = datetime(2025, 11, 13)
        mock_pr.head.ref = "feature"
        mock_pr.base.ref = "main"
        mock_pr.body = "Detailed PR description"
        mock_pr.user.login = "testuser"
        mock_pr.mergeable = True
        mock_pr.merged = False

        mock_repo.get_pull.return_value = mock_pr
        mock_github.return_value.get_repo.return_value = mock_repo

        # Execute
        request = GetPRRequest(repo="owner/repo", pr_number=10)
        response = service.get_pr(request)

        # Verify
        assert response.pull_request.number == 10
        assert response.pull_request.body == "Detailed PR description"
        assert response.pull_request.mergeable is True


class TestGetFileContentsTool:
    """Test get_file_contents tool implementation."""

    @pytest.fixture
    def mock_github(self):
        """Mock PyGithub client."""
        with patch("chora_github.core.services.Github") as mock:
            yield mock

    @pytest.fixture
    def service(self, mock_github):
        """Create service instance with mocked Github client."""
        from chora_github.core.services import GithubToolService

        return GithubToolService(token="ghp_test_token")

    def test_get_file_contents_success(self, service, mock_github):
        """Test successful get_file_contents call."""
        from chora_github.core.models import GetFileContentsRequest

        # Mock
        mock_repo = Mock()
        mock_file = Mock()
        mock_file.path = "README.md"
        mock_file.decoded_content = b"# Test Repository\n\nContent here."
        mock_file.size = 35
        mock_file.sha = "abc123"

        mock_repo.get_contents.return_value = mock_file
        mock_github.return_value.get_repo.return_value = mock_repo

        # Execute
        request = GetFileContentsRequest(repo="owner/repo", path="README.md")
        response = service.get_file_contents(request)

        # Verify
        assert response.path == "README.md"
        assert "Test Repository" in response.content
        assert response.size == 35
        assert response.sha == "abc123"


class TestListRepoFilesTool:
    """Test list_repo_files tool implementation."""

    @pytest.fixture
    def mock_github(self):
        """Mock PyGithub client."""
        with patch("chora_github.core.services.Github") as mock:
            yield mock

    @pytest.fixture
    def service(self, mock_github):
        """Create service instance with mocked Github client."""
        from chora_github.core.services import GithubToolService

        return GithubToolService(token="ghp_test_token")

    def test_list_repo_files_success(self, service, mock_github):
        """Test successful list_repo_files call."""
        from chora_github.core.models import ListRepoFilesRequest

        # Mock
        mock_repo = Mock()
        mock_file = Mock()
        mock_file.name = "README.md"
        mock_file.path = "README.md"
        mock_file.type = "file"
        mock_file.size = 1024
        mock_file.sha = "abc123"

        mock_dir = Mock()
        mock_dir.name = "src"
        mock_dir.path = "src"
        mock_dir.type = "dir"
        mock_dir.size = 0
        mock_dir.sha = "def456"

        mock_repo.get_contents.return_value = [mock_file, mock_dir]
        mock_github.return_value.get_repo.return_value = mock_repo

        # Execute
        request = ListRepoFilesRequest(repo="owner/repo")
        response = service.list_repo_files(request)

        # Verify
        assert response.total_count == 2
        assert response.files[0].name == "README.md"
        assert response.files[0].type == "file"
        assert response.files[1].name == "src"
        assert response.files[1].type == "dir"
