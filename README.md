# Bookmark URL Shortener API

A FastAPI application that allows users to:
- Register and login
- Create bookmark URLs
- Get shortened URLs
- Track bookmark visit counts

## Features

- User authentication with JWT
- Bookmark creation and management
- URL shortening with unique codes
- Visit tracking for shortened URLs
- RESTful API

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Database Migration

* create a new database `bookmark_shortener`
* run the alembic migration to create the tables
```bash
alembic init alembic
alembic revision --autogenerate -m "first commit"
alembic upgrade head
```

## Running the Application

```
python run.py
```

The API will be available at http://localhost:8000

## API Documentation

- Interactive API documentation is available at `/docs` (Swagger UI)
- Alternative API documentation is available at `/redoc` (ReDoc)

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/token` - Login and get access token

### Bookmarks

- `POST /bookmarks/` - Create a new bookmark
- `GET /bookmarks/` - Get all user bookmarks
- `GET /bookmarks/{bookmark_id}` - Get a specific bookmark
- `DELETE /bookmarks/{bookmark_id}` - Delete a bookmark

### URL Redirects

- `GET /{short_code}` - Redirect to original URL and increment visit count