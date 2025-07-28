"""
Utility functions for classifying PR types and priorities.
"""
from typing import Dict, List


def classify_pr_type(labels: List[Dict], title: str, body: str) -> str:
    """Classify PR type based on labels and content."""
    label_names = [label.get("name", "").lower() for label in labels]
    content = f"{title} {body}".lower()
    
    # Check for specific label types
    if any(label in ["feature", "enhancement", "new-feature"] for label in label_names):
        return "feature"
    elif any(label in ["bug", "bugfix", "fix"] for label in label_names):
        return "bugfix"
    elif any(label in ["docs", "documentation"] for label in label_names):
        return "docs"
    elif any(label in ["refactor", "refactoring"] for label in label_names):
        return "refactor"
    
    # Check content for type indicators
    if any(word in content for word in ["fix", "bug", "issue", "problem"]):
        return "bugfix"
    elif any(word in content for word in ["feature", "add", "new", "implement"]):
        return "feature"
    elif any(word in content for word in ["doc", "readme", "comment"]):
        return "docs"
    elif any(word in content for word in ["refactor", "clean", "improve"]):
        return "refactor"
    
    # Default to feature
    return "feature"


def classify_priority(labels: List[Dict], title: str, body: str) -> str:
    """Classify PR priority based on labels and content."""
    label_names = [label.get("name", "").lower() for label in labels]
    content = f"{title} {body}".lower()
    
    # Check for priority labels
    if any(label in ["urgent", "critical", "hotfix"] for label in label_names):
        return "urgent"
    elif any(label in ["high", "high-priority"] for label in label_names):
        return "high"
    elif any(label in ["low", "low-priority"] for label in label_names):
        return "low"
    
    # Check content for priority indicators
    if any(word in content for word in ["urgent", "critical", "hotfix", "emergency"]):
        return "urgent"
    elif any(word in content for word in ["high", "important", "blocking"]):
        return "high"
    elif any(word in content for word in ["low", "minor", "nice-to-have"]):
        return "low"
    
    # Default to medium priority
    return "medium"


def get_assignee(assignees: List[Dict]) -> str:
    """Extract assignee from assignees list."""
    if assignees and len(assignees) > 0:
        return assignees[0].get("login", "")
    return ""


def analyze_pr_data(pr_data: Dict) -> Dict:
    """Analyze PR data and return metadata."""
    labels = pr_data.get("labels", [])
    title = pr_data.get("title", "")
    body = pr_data.get("body", "")
    assignees = pr_data.get("assignees", [])
    
    return {
        "pr_type": classify_pr_type(labels, title, body),
        "priority": classify_priority(labels, title, body),
        "assignee": get_assignee(assignees)
    } 