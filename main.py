import os
from dotenv import load_dotenv

from fastapi import FastAPI, Response, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from fasthx import Jinja

# Import from our modular structure
from app.models.pr_models import User, PRDescriptionRequest, PRDescriptionResponse, PRReviewRequest, PRReviewResponse
from app.services.github_service import parse_github_pr_url, fetch_github_pr_data
from app.services.openai_service import generate_pr_description_with_openai
from app.services.pr_review_service import generate_pr_review_with_openai
from app.utils.pr_classifier import analyze_pr_data

# Load environment variables from .env file
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the app instance.
app = FastAPI()

# Create a FastAPI Jinja2Templates instance. This will be used in FastHX Jinja instance.
templates = Jinja2Templates(directory=os.path.join(basedir, "templates"))

# FastHX Jinja instance is initialized with the Jinja2Templates instance.
jinja = Jinja(templates)


@app.post("/generate-pr-description")
@jinja.hx("pr-description/pr-description-result.html", no_data=True)
def generate_pr_description(pr_url: str = Form(...)) -> PRDescriptionResponse:
    """Generate PR description from GitHub URL."""
    # Parse GitHub PR URL
    owner, repo, pr_number = parse_github_pr_url(pr_url)
    
    # Fetch PR data from GitHub
    github_data = fetch_github_pr_data(owner, repo, pr_number)
    
    # Generate AI description
    generated_description = generate_pr_description_with_openai(github_data)
    
    # Determine PR type and priority based on labels
    metadata = analyze_pr_data(github_data)
    pr_type = metadata["pr_type"]
    priority = metadata["priority"]
    assignee = metadata["assignee"]

    return PRDescriptionResponse(
        title=github_data.get("title", "Unknown PR"),
        repository=github_data.get("repository", "Unknown repository"),
        description=github_data.get("body", ""),
        pr_type=pr_type,
        priority=priority,
        assignee=assignee,
        generated_description=generated_description,
        github_data=github_data,
    )


@app.get("/user-list")
@jinja.hx("user-list.html")  # Render the response with the user-list.html template.
def htmx_or_data(response: Response) -> tuple[User, ...]:
    """This route can serve both JSON and HTML, depending on if the request is an HTMX request or not."""
    response.headers["my-response-header"] = "works"
    return (
        User(first_name="Peter", last_name="Volf"),
        User(first_name="Hasan", last_name="Tasan"),
    )


@app.get("/admin-list")
@jinja.hx(
    "user-list.html", no_data=True
)  # Render the response with the user-list.html template.
def htmx_only() -> list[User]:
    """This route can only serve HTML, because the no_data parameter is set to True."""
    return [User(first_name="John", last_name="Doe")]


@app.get("/")
def index(request: Request) -> Response:
    """This route serves the index.html template."""
    # Check if this is an HTMX request
    if request.headers.get("HX-Request"):
        # Return partial content for HTMX requests (just the main content)
        return templates.TemplateResponse("dashboard/dashboard-content.html", {"request": request})
    else:
        # Return full page for regular requests
        return templates.TemplateResponse("dashboard/index.html", {"request": request})


@app.get("/pr-description")
def pr_description(request: Request) -> Response:
    """This route serves the pr-description.html template."""
    # Check if this is an HTMX request
    if request.headers.get("HX-Request"):
        # Return partial content for HTMX requests (just the main content)
        return templates.TemplateResponse("pr-description/pr-description-content.html", {"request": request})
    else:
        # Return full page for regular requests
        return templates.TemplateResponse("pr-description/pr-description.html", {"request": request})


@app.get("/pr-review")
def pr_review(request: Request) -> Response:
    """This route serves the pr-review.html template."""
    # Check if this is an HTMX request
    if request.headers.get("HX-Request"):
        # Return partial content for HTMX requests (just the main content)
        return templates.TemplateResponse("pr-review/pr-review-content.html", {"request": request})
    else:
        # Return full page for regular requests
        return templates.TemplateResponse("pr-review/pr-review.html", {"request": request})


@app.post("/generate-pr-review")
@jinja.hx("pr-review/pr-review-result.html", no_data=True)
def generate_pr_review(pr_url: str = Form(...)) -> PRReviewResponse:
    """Generate PR review from GitHub URL."""
    # Parse GitHub PR URL
    owner, repo, pr_number = parse_github_pr_url(pr_url)
    
    # Fetch PR data from GitHub
    github_data = fetch_github_pr_data(owner, repo, pr_number)
    
    # Generate AI review
    review_analysis, review_score = generate_pr_review_with_openai(github_data)
    
    # Determine PR type and priority based on labels
    metadata = analyze_pr_data(github_data)
    pr_type = metadata["pr_type"]
    priority = metadata["priority"]
    assignee = metadata["assignee"]

    return PRReviewResponse(
        title=github_data.get("title", "Unknown PR"),
        repository=github_data.get("repository", "Unknown repository"),
        pr_type=pr_type,
        priority=priority,
        assignee=assignee,
        review_analysis=review_analysis,
        review_score=review_score,
        github_data=github_data,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
