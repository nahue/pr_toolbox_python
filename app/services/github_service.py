"""
GitHub API service for fetching pull request data.
"""
import os
import requests
from urllib.parse import urlparse
from fastapi import HTTPException
from typing import Dict, Tuple


def parse_github_pr_url(url: str) -> Tuple[str, str, int]:
    """Parse GitHub PR URL to extract owner, repo, and PR number."""
    try:
        parsed = urlparse(url)
        if parsed.netloc != "github.com":
            raise ValueError("Not a GitHub URL")

        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) < 4 or path_parts[2] != "pull":
            raise ValueError("Invalid GitHub PR URL format")

        owner = path_parts[0]
        repo = path_parts[1]
        pr_number = int(path_parts[3])

        return owner, repo, pr_number
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=400, detail=f"Invalid GitHub PR URL: {str(e)}")


def fetch_github_pr_data(owner: str, repo: str, pr_number: int) -> Dict:
    """Fetch PR data from GitHub API."""
    github_token = os.getenv("GITHUB_TOKEN")

    if not github_token:
        # Fallback to mock data if no token is provided
        return _get_mock_pr_data(owner, repo, pr_number)

    # GitHub API endpoint for pull requests
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "PR-Toolbox-App",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        pr_data = response.json()

        # Fetch additional data
        labels = _fetch_pr_labels(owner, repo, pr_number, headers)
        files_changed = _fetch_pr_files(owner, repo, pr_number, headers)

        return {
            "title": pr_data.get("title", "Unknown PR"),
            "body": pr_data.get("body", ""),
            "user": pr_data.get("user", {}),
            "assignees": pr_data.get("assignees", []),
            "labels": labels,
            "state": pr_data.get("state", "open"),
            "created_at": pr_data.get("created_at", ""),
            "updated_at": pr_data.get("updated_at", ""),
            "changed_files": files_changed,
            "additions": pr_data.get("additions", 0),
            "deletions": pr_data.get("deletions", 0),
            "repository": f"{owner}/{repo}",
            "pr_number": pr_number,
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching GitHub data: {e}")
        return _get_mock_pr_data(owner, repo, pr_number)


def _fetch_pr_labels(owner: str, repo: str, pr_number: int, headers: Dict) -> list:
    """Fetch PR labels from GitHub API."""
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/labels"
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return []


def _fetch_pr_files(owner: str, repo: str, pr_number: int, headers: Dict) -> int:
    """Fetch number of files changed in PR."""
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        files = response.json()
        return len(files)
    except requests.exceptions.RequestException:
        return 0


def _get_mock_pr_data(owner: str, repo: str, pr_number: int) -> Dict:
    """Return mock PR data for testing or when GitHub token is not available."""
    return {
        "title": f"Sample PR #{pr_number}",
        "body": "This is a sample PR description that would be fetched from GitHub.",
        "user": {"login": "sample-user"},
        "assignees": [{"login": "assignee-user"}],
        "labels": [{"name": "enhancement"}],
        "state": "open",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "changed_files": 5,
        "additions": 100,
        "deletions": 20,
        "repository": f"{owner}/{repo}",
        "pr_number": pr_number,
    } 