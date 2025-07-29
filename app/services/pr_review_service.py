"""
PR Review service for generating AI-powered pull request reviews.
"""
import os
import requests
from typing import Dict


def generate_pr_review_with_openai(pr_data: Dict) -> tuple[str, int]:
    """Generate PR review using OpenAI."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        # Fallback to mock review if no API key is provided
        return _get_mock_review(pr_data), _get_mock_score(pr_data)

    prompt = _build_pr_review_prompt(pr_data)

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
                    "content": "You are an expert software developer and code reviewer. Please provide a comprehensive, constructive review of the pull request. Focus on code quality, potential issues, security concerns, and suggestions for improvement. Be thorough but fair."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": 1500,
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
        review_analysis = result["choices"][0]["message"]["content"]
        
        # Generate a review score based on the analysis
        review_score = _generate_review_score(review_analysis, pr_data)
        
        return review_analysis.strip(), review_score
        
    except requests.exceptions.RequestException as e:
        print(f"Error calling OpenAI API: {e}")
        return _get_error_review(str(e)), 5
    except (KeyError, IndexError) as e:
        print(f"Error parsing OpenAI response: {e}")
        return _get_error_review("Unexpected response format"), 5


def _build_pr_review_prompt(pr_data: Dict) -> str:
    """Build the prompt for OpenAI based on PR data."""
    title = pr_data.get("title", "Unknown PR")
    body = pr_data.get("body", "")
    labels = [label.get("name", "") for label in pr_data.get("labels", [])]
    assignees = [assignee.get("login", "") for assignee in pr_data.get("assignees", [])]
    changed_files = pr_data.get("changed_files", 0)
    additions = pr_data.get("additions", 0)
    deletions = pr_data.get("deletions", 0)
    repository = pr_data.get("repository", "Unknown repository")
    
    prompt = f"""Please provide a comprehensive code review for the following pull request:

**PR Title:** {title}
**Repository:** {repository}
**Original Description:** {body}
**Labels:** {', '.join(labels) if labels else 'None'}
**Assignees:** {', '.join(assignees) if assignees else 'None'}
**Files Changed:** {changed_files}
**Additions:** {additions} lines
**Deletions:** {deletions} lines

Please structure your review with the following sections:

1. **Overall Assessment** - Brief summary of the changes and their impact
2. **Code Quality** - Analysis of code structure, readability, and best practices
3. **Potential Issues** - Any bugs, security concerns, or edge cases
4. **Suggestions** - Recommendations for improvement
5. **Testing** - Comments on test coverage and testing approach
6. **Documentation** - Assessment of code documentation and comments

Be constructive, specific, and actionable in your feedback. Focus on helping the developer improve the code while maintaining a positive tone."""
    
    return prompt


def _generate_review_score(review_analysis: str, pr_data: Dict) -> int:
    """Generate a review score (1-10) based on the analysis and PR data."""
    # This is a simplified scoring algorithm
    # In a real implementation, you might use more sophisticated analysis
    
    score = 7  # Base score
    
    # Adjust based on review content
    review_lower = review_analysis.lower()
    
    # Positive indicators
    if any(word in review_lower for word in ["good", "excellent", "well", "clean", "clear"]):
        score += 1
    if any(word in review_lower for word in ["tests", "testing", "coverage"]):
        score += 1
    if any(word in review_lower for word in ["documentation", "comments", "readable"]):
        score += 1
    
    # Negative indicators
    if any(word in review_lower for word in ["issue", "problem", "bug", "security"]):
        score -= 1
    if any(word in review_lower for word in ["refactor", "improve", "better"]):
        score -= 1
    
    # Adjust based on PR characteristics
    changed_files = pr_data.get("changed_files", 0)
    if changed_files > 10:
        score -= 1  # Large changes are riskier
    elif changed_files < 3:
        score += 1  # Small changes are generally safer
    
    # Ensure score is between 1 and 10
    return max(1, min(10, score))


def _get_mock_review(pr_data: Dict) -> str:
    """Return a mock review for testing or when OpenAI API key is not available."""
    title = pr_data.get("title", "Unknown PR")
    repository = pr_data.get("repository", "Unknown repository")
    
    return f"""## Overall Assessment
This pull request {title.lower()} in the {repository} repository appears to be a well-structured change.

## Code Quality
- The code follows good practices and is generally readable
- Variable naming is clear and descriptive
- Functions are appropriately sized and focused

## Potential Issues
- Consider adding more error handling for edge cases
- Some functions could benefit from additional input validation

## Suggestions
- Add unit tests for the new functionality
- Consider adding more inline documentation
- Review the error handling approach

## Testing
- Ensure comprehensive test coverage for new features
- Add integration tests if applicable
- Consider edge case testing

## Documentation
- Code is generally self-documenting
- Consider adding more detailed comments for complex logic
- Update any relevant documentation

**Note:** This is a sample review generated when OpenAI API is not available. Please configure your OpenAI API key for AI-powered reviews."""


def _get_mock_score(pr_data: Dict) -> int:
    """Return a mock score for testing."""
    return 7


def _get_error_review(error_message: str) -> str:
    """Return an error review when API calls fail."""
    return f"""## Overall Assessment
Unable to generate AI review due to API error: {error_message}

## Code Quality
Please review the code manually for:
- Code structure and organization
- Readability and maintainability
- Adherence to coding standards

## Potential Issues
- Check for potential bugs and edge cases
- Review security implications
- Verify error handling

## Suggestions
- Consider code review best practices
- Look for opportunities to improve
- Ensure proper testing coverage

## Testing
- Verify all functionality works as expected
- Check test coverage
- Perform manual testing

## Documentation
- Review code comments and documentation
- Ensure changes are properly documented

**Note:** AI-powered review generation failed. Please review the code manually."""