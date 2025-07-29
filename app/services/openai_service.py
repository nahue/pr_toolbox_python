"""
OpenAI API service for generating PR descriptions.
"""
import os
import requests
from typing import Dict


def generate_pr_description_with_openai(pr_data: Dict) -> str:
    """Generate PR description using OpenAI."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        # Fallback to mock description if no API key is provided
        return _get_mock_description(pr_data)

    prompt = _build_pr_description_prompt(pr_data)

    try:
        headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are an expert software developer and technical writer. Please create comprehensive, professional pull request descriptions based on GitHub PR data. Focus on clarity, technical accuracy, and helpfulness for reviewers."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", 
            headers=headers, 
            json=data, 
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        generated_description = result["choices"][0]["message"]["content"]
        return generated_description.strip()
        
    except requests.exceptions.RequestException as e:
        print(f"Error calling OpenAI API: {e}")
        return _get_error_description(str(e))
    except (KeyError, IndexError) as e:
        print(f"Error parsing OpenAI response: {e}")
        return _get_error_description("Unexpected response format")


def _build_pr_description_prompt(pr_data: Dict) -> str:
    """Build the prompt for OpenAI based on PR data."""
    title = pr_data.get("title", "Unknown PR")
    body = pr_data.get("body", "")
    labels = [label.get("name", "") for label in pr_data.get("labels", [])]
    assignees = [assignee.get("login", "") for assignee in pr_data.get("assignees", [])]
    changed_files = pr_data.get("changed_files", 0)
    additions = pr_data.get("additions", 0)
    deletions = pr_data.get("deletions", 0)
    repository = pr_data.get("repository", "Unknown repository")
    contributors = pr_data.get("contributors", [])
    
    # Format contributors information
    contributors_info = ""
    if contributors:
        contributors_list = []
        for contributor in contributors:
            login = contributor.get("login", "")
            name = contributor.get("name", login)
            contributions = contributor.get("contributions", 0)
            contributors_list.append(f"@{login} ({name}) - {contributions} commit{'s' if contributions != 1 else ''}")
        contributors_info = "\n".join(contributors_list)
    else:
        contributors_info = "No contributors found"
    
    prompt = f"""Please create a comprehensive, professional pull request description based on the following GitHub PR data:

**PR Title:** {title}
**Repository:** {repository}
**Original Description:** {body}
**Labels:** {', '.join(labels) if labels else 'None'}
**Assignees:** {', '.join(assignees) if assignees else 'None'}
**Files Changed:** {changed_files}
**Additions:** {additions} lines
**Deletions:** {deletions} lines
**Contributors:**
{contributors_info}

Please structure the description with the following sections:
1. **Summary** - Brief overview of what the PR accomplishes
2. **Changes Made** - Detailed list of changes and improvements
3. **Testing** - Information about testing performed
4. **Screenshots** (if applicable) - Visual changes
5. **Additional Notes** - Any other relevant information
6. **Contributors** - List of contributors to the PR with their contribution counts

Make the description clear, professional, and helpful for code reviewers. Focus on the "why" and "what" of the changes. Include the contributors section to acknowledge all team members who contributed to this PR."""
    
    return prompt


def _get_mock_description(pr_data: Dict) -> str:
    """Return a mock description for testing or when OpenAI API key is not available."""
    title = pr_data.get("title", "Unknown PR")
    repository = pr_data.get("repository", "Unknown repository")
    contributors = pr_data.get("contributors", [])
    
    # Format contributors for mock description
    contributors_section = ""
    if contributors:
        contributors_list = []
        for contributor in contributors:
            login = contributor.get("login", "")
            name = contributor.get("name", login)
            contributions = contributor.get("contributions", 0)
            contributors_list.append(f"- @{login} ({name}) - {contributions} commit{'s' if contributions != 1 else ''}")
        contributors_section = "\n".join(contributors_list)
    else:
        contributors_section = "- No contributors found"
    
    return f"""## Summary
This pull request {title.lower()} in the {repository} repository.

## Changes Made
- Sample changes and improvements
- Code refactoring and optimization
- Bug fixes and enhancements

## Testing
- Unit tests have been added/updated
- Manual testing completed
- Integration tests passing

## Screenshots
N/A

## Additional Notes
This is a sample description generated when OpenAI API is not available. Please configure your OpenAI API key for AI-powered descriptions.

## Contributors
{contributors_section}"""


def _get_error_description(error_message: str) -> str:
    """Return an error description when API calls fail."""
    return f"""## Summary
Unable to generate AI description due to API error: {error_message}

## Changes Made
Please review the original PR description and manually create a comprehensive description.

## Testing
- Verify all changes work as expected
- Run existing test suite
- Perform manual testing

## Screenshots
N/A

## Additional Notes
The AI description generation failed. Please check your API configuration and try again.

## Contributors
Please manually review the PR commits to identify all contributors.""" 