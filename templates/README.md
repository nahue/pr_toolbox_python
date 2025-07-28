# Templates Structure

This directory contains all Jinja2 HTML templates organized by module for better maintainability and clarity.

## Directory Structure

```
templates/
├── shared/                    # Shared templates used across modules
│   └── base.html             # Base layout template with navigation
├── dashboard/                 # Dashboard module templates
│   ├── index.html            # Dashboard full page (extends base)
│   └── dashboard-content.html # Dashboard partial content (HTMX)
├── pr-description/           # PR Description module templates
│   ├── pr-description.html   # PR Description full page (extends base)
│   ├── pr-description-content.html # PR Description partial (HTMX)
│   └── pr-description-result.html  # PR Description result display
└── user/                     # User module templates
    └── user-list.html        # User list partial template
```

## Template Types

### Full Page Templates
- **Purpose**: Complete HTML pages that extend the base layout
- **Location**: Module-specific directories
- **Usage**: Regular page loads (non-HTMX requests)
- **Examples**: 
  - `dashboard/index.html`
  - `pr-description/pr-description.html`

### Partial Templates
- **Purpose**: Content fragments for HTMX requests
- **Location**: Module-specific directories
- **Usage**: HTMX content swaps
- **Examples**:
  - `dashboard/dashboard-content.html`
  - `pr-description/pr-description-content.html`
  - `pr-description/pr-description-result.html`

### Shared Templates
- **Purpose**: Reusable layout and components
- **Location**: `shared/` directory
- **Usage**: Extended by full page templates
- **Examples**:
  - `shared/base.html`

## Template Organization Principles

### 1. Module-Based Organization
- Templates are grouped by functional module
- Each module has its own directory
- Clear separation of concerns

### 2. HTMX Integration
- Full page templates for direct navigation
- Partial templates for HTMX requests
- Consistent naming convention

### 3. Reusability
- Shared base template for consistent layout
- Modular includes for content reuse
- Clear dependency structure

## Template Naming Convention

### Full Page Templates
- `index.html` - Main page for each module
- `{module-name}.html` - Specific feature pages

### Partial Templates
- `{module-name}-content.html` - Main content area
- `{module-name}-result.html` - Result displays
- `{module-name}-list.html` - List components

### Shared Templates
- `base.html` - Base layout template
- `components/` - Reusable UI components (future)

## Usage Examples

### Dashboard Module
```python
# Full page load
return templates.TemplateResponse("dashboard/index.html", {"request": request})

# HTMX request
return templates.TemplateResponse("dashboard/dashboard-content.html", {"request": request})
```

### PR Description Module
```python
# Full page load
return templates.TemplateResponse("pr-description/pr-description.html", {"request": request})

# HTMX request
return templates.TemplateResponse("pr-description/pr-description-content.html", {"request": request})

# HTMX result
@jinja.hx("pr-description/pr-description-result.html")
```

## Adding New Templates

### 1. Create Module Directory
```bash
mkdir templates/new-module/
```

### 2. Create Full Page Template
```html
<!-- templates/new-module/index.html -->
{% extends 'shared/base.html' %}
{% block content %}
{% include 'new-module/new-module-content.html' %}
{% endblock %}
```

### 3. Create Partial Template
```html
<!-- templates/new-module/new-module-content.html -->
<div class="bg-white shadow rounded-lg">
    <!-- Module content -->
</div>
```

### 4. Update Routes
```python
# Full page
return templates.TemplateResponse("new-module/index.html", {"request": request})

# HTMX
return templates.TemplateResponse("new-module/new-module-content.html", {"request": request})
```

## Best Practices

1. **Consistent Structure**: Follow the established pattern for new modules
2. **Clear Naming**: Use descriptive names that indicate purpose
3. **HTMX Ready**: Design templates with HTMX in mind
4. **Reusable Components**: Extract common patterns into shared templates
5. **Documentation**: Update this README when adding new templates