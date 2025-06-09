# LCDP Backend

A Django REST Framework backend for a Low-Code Development Platform.

## Features

- Page model for storing layout configurations
- Component model for UI elements
- RESTful API for CRUD operations
- CORS support for frontend integration

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd lcdp-backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

The API will be available at http://localhost:8000/api/

## API Endpoints

- Pages: `/api/pages/`
- Components: `/api/components/`

## Sample Request

### Creating a Page

POST to `/api/pages/`

```json
{
  "name": "Dashboard",
  "layout_config": {
    "rows": [
      {
        "columns": [
          {
            "width": 6,
            "components": [
              {
                "id": "chart1",
                "type": "chart"
              }
            ]
          },
          {
            "width": 6,
            "components": [
              {
                "id": "table1",
                "type": "table"
              }
            ]
          }
        ]
      }
    ]
  }
}
```

### Creating a Component

POST to `/api/components/`

```json
{
  "page": 1,
  "type": "button",
  "properties": {
    "label": "Submit",
    "color": "primary",
    "action": {
      "type": "submit",
      "target": "form1"
    }
  }
}
```

## Front-end Integration

This backend is configured to work with a React frontend running on `http://localhost:3000`. 