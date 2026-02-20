# Quick Ref ⚡

A containerized web application for storing and organizing your developer references, snippets, and quick commands. Perfect for keeping commonly-used code, Docker commands, Git workflows, and more in one searchable place.

## Features

- 📝 Create, read, update, and delete references
- 🔍 Full-text search across all references  
- 📂 Organize references by category
- 🎨 Clean, modern web interface
- 🐳 Fully containerized with Docker
- 🔧 RESTful API backend
- 💾 SQLite database for persistence
- ⚡ Fast and responsive UI

## Tech Stack

- **Backend:** Python Flask + Flask-CORS
- **Frontend:** Vanilla HTML5, CSS3, JavaScript
- **Database:** SQLite
- **Containerization:** Docker & Docker Compose

## Quick Start

### Using Docker Compose (Recommended)

1. Clone or download this project
2. Navigate to the project directory
3. Run:
   ```bash
   docker-compose up -d
   ```
4. Open your browser to `http://localhost:5000`

### Local Development

1. Install Python 3.11+
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python backend/app.py
   ```
5. Open `http://localhost:5000` in your browser

## Usage

### Web Interface

1. **Search**: Use the search box to find references by title or content
2. **Filter by Category**: Click on a category in the sidebar to filter references
3. **Add Reference**: Click "+ Add Reference" to create a new entry
4. **Edit Reference**: Click "Edit" on any reference to modify it
5. **Delete Reference**: Click "Delete" to remove a reference

### API Endpoints

- `GET /api/references` - Get all references (supports `?search=` and `?category=` query parameters)
- `POST /api/references` - Create a new reference
- `GET /api/references/<id>` - Get a specific reference
- `PUT /api/references/<id>` - Update a reference
- `DELETE /api/references/<id>` - Delete a reference
- `GET /api/categories` - Get all available categories
- `GET /health` - Health check endpoint

### Example API Usage

```bash
# Get all references
curl http://localhost:5000/api/references

# Search for references
curl "http://localhost:5000/api/references?search=docker"

# Filter by category
curl "http://localhost:5000/api/references?category=Python"

# Create a new reference
curl -X POST http://localhost:5000/api/references \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Docker Compose",
    "category": "Docker",
    "content": "docker-compose up -d\ndocker-compose logs -f",
    "language": "bash"
  }'
```

## Project Structure

```
quick-ref/
├── backend/
│   └── app.py              # Flask application and API
├── frontend/
│   └── index.html          # Web interface
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Multi-container orchestration
├── requirements.txt        # Python dependencies
├── .dockerignore           # Files to exclude from Docker build
├── .gitignore              # Git ignore patterns
└── README.md              # This file
```

## Configuration

### Environment Variables

You can set environment variables in `docker-compose.yml`:

- `FLASK_ENV` - Set to `production` for production use (default: `production`)
- `FLASK_DEBUG` - Set to `1` to enable debug mode (default: `0`)

### Database

The SQLite database (`references.db`) is created automatically on first run. It includes sample data to get you started.

To persist data across container restarts, the Docker Compose configuration volumes the `data/` directory.

## Development

### Adding More Languages to the Frontend

Edit the `<select>` element for language in `frontend/index.html` to add more syntax highlighting languages.

### Extending the API

The Flask app in `backend/app.py` can be easily extended with additional endpoints or features:

- Authentication/authorization
- User management
- Tags instead of just categories
- Export to PDF/Markdown
- API rate limiting

## Troubleshooting

### Port 5000 already in use

Change the port in `docker-compose.yml`:
```yaml
ports:
  - "8080:5000"  # Access at http://localhost:8080
```

### Database issues

To reset the database, delete `references.db` and restart the container:
```bash
docker-compose down
rm references.db
docker-compose up -d
```

### Container won't start

Check the logs:
```bash
docker-compose logs -f quick-ref
```

## License

MIT License - Feel free to use this project for personal or commercial purposes.

## Contributing

Suggestions and improvements are welcome! Feel free to fork and improve.

---

**Quick Ref** - Keep your references quick and close! ⚡
