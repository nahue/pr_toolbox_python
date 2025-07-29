"""
Pydantic models for PR-related data structures.
"""
from pydantic import BaseModel
from typing import Dict, List, Optional


class User(BaseModel):
    """User model for basic user information."""
    first_name: str
    last_name: str


class PRDescriptionRequest(BaseModel):
    """Request model for PR description generation."""
    pr_url: str


class PRDescriptionResponse(BaseModel):
    """Response model for generated PR description."""
    title: str
    repository: str
    description: str
    pr_type: str
    priority: str
    assignee: str
    generated_description: str
    github_data: Dict


class PRReviewRequest(BaseModel):
    """Request model for PR review generation."""
    pr_url: str


class PRReviewResponse(BaseModel):
    """Response model for generated PR review."""
    title: str
    repository: str
    pr_type: str
    priority: str
    assignee: str
    review_analysis: str
    review_score: int
    github_data: Dict


class GitHubPRData(BaseModel):
    """Model for GitHub PR data structure."""
    title: str
    body: Optional[str] = ""
    user: Dict
    assignees: List[Dict]
    labels: List[Dict]
    state: str
    created_at: str
    updated_at: str
    changed_files: int
    additions: int
    deletions: int
    repository: str
    pr_number: int


class PRMetadata(BaseModel):
    """Model for PR metadata and classification."""
    pr_type: str
    priority: str
    assignee: Optional[str] = None 