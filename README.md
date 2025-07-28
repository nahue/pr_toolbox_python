# PR Toolbox

A modern web application for generating AI-powered pull request descriptions using GitHub API and OpenAI.

## Features

- **AI-Powered PR Descriptions**: Generate comprehensive PR descriptions using OpenAI
- **GitHub Integration**: Fetch real PR data from GitHub repositories
- **Modern UI**: Built with FastAPI, HTMX, and Tailwind CSS
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: HTMX-powered dynamic content loading

## Project Structure

```
pr-toolbox-uv/
├── app/                          # Main application package
│   ├── models/                   # Pydantic data models
│   │   ├── __init__.py
│   │   └── pr_models.py         # PR-related data models
│   ├── services/                 # External service integrations
│   │   ├── __init__.py
│   │   ├── github_service.py    # GitHub API integration
│   │   └── openai_service.py    # OpenAI API integration
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       └── pr_classifier.py     # PR classification utilities
├── templates/                    # Jinja2 HTML templates (modular)
│   ├── shared/                  # Shared templates
│   │   └── base.html           # Base layout template
│   ├── dashboard/               # Dashboard module templates
│   │   ├── index.html          # Dashboard full page
│   │   └── dashboard-content.html # Dashboard partial content
│   ├── pr-description/         # PR Description module templates
│   │   ├── pr-description.html # PR Description full page
│   │   ├── pr-description-content.html # PR Description partial
│   │   └── pr-description-result.html  # PR Description result
│   └── user/                   # User module templates
│       └── user-list.html      # User list partial
├── main.py                      # FastAPI application entry point
├── pyproject.toml               # Project dependencies and configuration
├── env.example                  # Environment variables template
└── README.md                    # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd pr-toolbox-uv
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application**:
   ```bash
   uv run main.py
   ```

## Environment Variables

Create a `.env` file with the following variables:

```env
# GitHub API Token (optional - will use mock data if not provided)
GITHUB_TOKEN=your_github_token_here

# OpenAI API Key (optional - will use mock descriptions if not provided)
OPENAI_API_KEY=your_openai_api_key_here

# Application settings
DEBUG=true
LOG_LEVEL=INFO
```

## Usage

1. **Start the application**: The app will be available at `http://localhost:8001`

2. **Navigate to PR Descriptions**: Click on "PR Descriptions" in the sidebar

3. **Enter a GitHub PR URL**: Paste a GitHub pull request URL (e.g., `https://github.com/owner/repo/pull/123`)

4. **Generate Description**: Click "Generate" to fetch PR data and create an AI-powered description

5. **View Results**: The generated description will appear with options to copy, save, or regenerate

## API Endpoints

- `GET /` - Dashboard page
- `GET /pr-description` - PR description generation page
- `POST /generate-pr-description` - Generate PR description from GitHub URL
- `GET /user-list` - User list (example endpoint)
- `GET /admin-list` - Admin list (example endpoint)

## Architecture

### Services

- **GitHub Service** (`app/services/github_service.py`): Handles GitHub API interactions
  - `parse_github_pr_url()`: Parse GitHub PR URLs
  - `fetch_github_pr_data()`: Fetch PR data from GitHub API
  - Mock data fallback when GitHub token is not available

- **OpenAI Service** (`app/services/openai_service.py`): Handles OpenAI API interactions
  - `generate_pr_description_with_openai()`: Generate PR descriptions using GPT
  - Smart prompt engineering for better results
  - Error handling and fallback descriptions

### Models

- **PR Models** (`app/models/pr_models.py`): Pydantic data models
  - `PRDescriptionRequest`: Input model for PR URL
  - `PRDescriptionResponse`: Output model for generated descriptions
  - `GitHubPRData`: GitHub PR data structure
  - `PRMetadata`: PR classification metadata

### Utils

- **PR Classifier** (`app/utils/pr_classifier.py`): PR analysis utilities
  - `classify_pr_type()`: Determine PR type (feature, bugfix, docs, etc.)
  - `classify_priority()`: Determine PR priority (urgent, high, medium, low)
  - `analyze_pr_data()`: Comprehensive PR data analysis

## Technologies Used

- **Backend**: FastAPI, Python 3.11+
- **Frontend**: HTMX, Tailwind CSS, Jinja2
- **APIs**: GitHub API, OpenAI API
- **Package Management**: uv
- **Development**: Type hints, Pydantic models

## Development

### Adding New Features

1. **Create new services** in `app/services/`
2. **Add data models** in `app/models/`
3. **Create utility functions** in `app/utils/`
4. **Add routes** in `main.py`
5. **Create templates** in `templates/`

### Code Organization

- **Separation of Concerns**: Each module has a specific responsibility
- **Dependency Injection**: Services are imported and used in routes
- **Error Handling**: Comprehensive error handling with fallbacks
- **Type Safety**: Full type hints throughout the codebase

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
