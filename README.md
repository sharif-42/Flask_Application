# Flask Bank Management System

A complete CRUD application built with Flask and Microsoft SQL Server to manage banks using Docker.

## Features

- **Full CRUD Operations**: Create, Read, Update, and Delete banks
- **Flask 3.1.2** web framework with Jinja2 templates
- **Microsoft SQL Server 2022** database support
- **Docker & Docker Compose** containerized development environment
- **SQL Server ODBC Driver 18** for database connectivity
- **Responsive UI** with modern CSS styling
- **Static Files Management** with dedicated static folder
- **Form Validation** for data integrity
- **Flash Messages** for user feedback
- **Error Handling** with custom 404 and 500 pages
- **Persistent Storage** with Docker volumes

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

## Quick Start with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd Flask_Application
```

2. Create environment file:
```bash
cp .env.example .env
```

Edit `.env` and update the configuration values, especially `SQL_PASSWORD`.

3. Start the application:
```bash
docker compose up --build
```

The application will be available at `http://localhost:5000`

The SQL Server will be available at `localhost:1433`

4. Stop the application:
```bash
docker compose down
```

To remove volumes (database data):
```bash
docker compose down -v
```

## Docker Configuration

### Services

The Docker Compose setup includes two services:

1. **sqlserver**: Microsoft SQL Server 2022 container
   - Port: 1433
   - Default SA password: `YourStrong@Passw0rd` (change in `.env`)
   - Persistent storage via Docker volume

2. **flask_app**: Flask application container
   - Port: 5000
   - Auto-reload enabled in development mode
   - Connected to SQL Server via Docker network

### Environment Variables

Configure the application using `.env` file:

```bash
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key

# SQL Server Configuration
SQL_DATABASE=flaskr_db
SQL_USERNAME=sa
SQL_PASSWORD=YourStrong@Passw0rd
```



## Running the Application

### With Docker

```bash
# Build and start services
docker compose up --build

# Run in background (detached mode)
docker compose up -d

# View logs
docker compose logs -f
docker compose logs -f flask_app
docker compose logs -f sqlserver

# Stop services
docker compose down

# Stop and remove volumes (deletes database data)
docker compose down -v

# Restart services
docker compose restart
```

### Accessing Containers

```bash
# Access Flask app container
docker compose exec flask_app bash

# Access SQL Server with sqlcmd
docker compose exec sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'YourStrong@Passw0rd' -C
```

### Database Initialization

After starting the containers, initialize the database:

```bash
docker compose exec sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'YourStrong@Passw0rd' -i /docker-entrypoint-initdb.d/init.sql -C
```

This creates the `banks` table with the required schema.

## Project Structure

```
Flask_Application/
├── flaskr/
│   ├── static/
│   │   └── css/
│   │       └── style.css            # Application styles
│   ├── templates/
│   │   ├── errors/
│   │   │   ├── 404.html             # Page not found error
│   │   │   └── 500.html             # Internal server error
│   │   ├── base.html                # Base template with navigation
│   │   ├── index.html               # Banks list page
│   │   ├── add_bank.html            # Add bank form
│   │   ├── edit_bank.html           # Edit bank form
│   │   └── bank_detail.html         # Bank details page
│   ├── __init__.py                  # Application factory and routes
│   └── db.py                        # Database CRUD operations
├── init-db/
│   └── init.sql                     # Database schema initialization
├── instance/                        # Instance-specific files (gitignored)
├── .dockerignore                    # Docker build exclusions
├── .env.example                     # Environment variables template
├── .env                             # Environment variables (gitignored)
├── .gitignore                       # Git exclusions
├── docker-compose.yml               # Docker Compose configuration
├── Dockerfile                       # Flask app Docker image
├── requirements.txt                 # Python dependencies
└── README.md                       # This file
```

## Application Routes

### Bank Management
- `GET /` - Display list of all banks in a table
- `GET /banks/add` - Show form to add a new bank
- `POST /banks/add` - Create a new bank
- `GET /banks/<id>` - Display details for a specific bank
- `GET /banks/<id>/edit` - Show form to edit a bank
- `POST /banks/<id>/edit` - Update an existing bank
- `POST /banks/<id>/delete` - Delete a bank (with confirmation)

### Error Pages
- `404` - Page not found error
- `500` - Internal server error

## Database Schema

The `banks` table contains:
- `id` (INT, PRIMARY KEY, IDENTITY) - Unique identifier
- `name` (NVARCHAR(255)) - Bank name
- `location` (NVARCHAR(255)) - Bank location
- `created_at` (DATETIME) - Creation timestamp
- `updated_at` (DATETIME) - Last update timestamp

## Using the Application

Once the Docker containers are running, open your browser and navigate to http://localhost:5000/

### Features Walkthrough

1. **View All Banks**: The home page displays all banks in a responsive table with ID, name, location, and creation date
2. **Add New Bank**: Click "Add Bank" in the navigation or the button on the page to access the form
3. **View Bank Details**: Click "View" on any bank to see full details including timestamps
4. **Edit Bank**: Click "Edit" from the list or detail page to update bank information
5. **Delete Bank**: Click "Delete" and confirm to remove a bank from the database

## Dependencies

- Flask 3.1.2
- Werkzeug 3.1.4
- Jinja2 3.1.6
- pyodbc 5.2.0
- python-dotenv 1.0.0

See `requirements.txt` for complete list.

## Database Connection

The application connects to SQL Server using the connection string format:

```python
DRIVER={ODBC Driver 18 for SQL Server};
SERVER=sqlserver;
DATABASE=flaskr_db;
UID=sa;
PWD=YourStrong@Passw0rd;
TrustServerCertificate=yes;
```

- **Server hostname**: `sqlserver` (Docker service name)
- **Connection**: Handled through `flaskr/db.py` with automatic connection pooling
- **Security**: TrustServerCertificate enabled for Docker environment

## Testing

This project includes integration-style pytest tests that run against the SQL Server container.

Basic workflow (no Compose file changes required):

1. Start the services (SQL Server + Flask app):

```bash
docker compose up -d
```

2. Ensure the `banks` table exists (run once; idempotent):

```bash
docker compose exec sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'YourStrong@Passw0rd' -i /docker-entrypoint-initdb.d/init.sql -C
```

3. Run tests from a container (recommended — one-off container):

```bash
docker compose run --rm flask_app pytest --maxfail=1 -q
```

Or run tests inside the already-running Flask container:

```bash
docker compose exec flask_app pytest --maxfail=1 -q
```

Notes:

- Tests assume the database name is `flaskr_db` and the `banks` table exists. Adjust `SQL_DATABASE` if you use a separate test database.
- If `pytest` or other dev dependencies are missing in the image, rebuild the Flask image so `requirements.txt` is installed:

```bash
docker compose build flask_app
docker compose up -d sqlserver flask_app
docker compose run --rm flask_app pytest -q
```

## Troubleshooting

### SQL Server Connection Issues

1. Ensure SQL Server container is healthy:
```bash
docker compose ps
```

2. Check SQL Server logs:
```bash
docker compose logs sqlserver
```

3. Test connection manually:
```bash
docker compose exec sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'YourStrong@Passw0rd' -C
```

### Flask Application Issues

1. Check Flask logs:
```bash
docker compose logs flask_app
```

2. Restart Flask service:
```bash
docker compose restart flask_app
```

3. Rebuild containers:
```bash
docker compose up --build
```

## Development Notes

- The application runs in **development mode** with Flask's built-in server
- Auto-reload is enabled for code changes
- Debug mode is off for security
- Static files are served from `flaskr/static/`
- Templates use Jinja2 template inheritance for consistency

## Technologies Used

- **Backend**: Flask 3.1.2 (Python web framework)
- **Database**: Microsoft SQL Server 2022
- **Database Driver**: pyodbc 5.2.0 with ODBC Driver 18
- **Containerization**: Docker & Docker Compose
- **Frontend**: HTML5, CSS3, Jinja2 templates
- **Configuration**: python-dotenv for environment variables

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.