# Flask Application

A Flask web application with SQL Server database integration support.

## Features

- Flask 3.1.2 web framework
- SQL Server database support (ODBC Driver 18)
- Custom error handling (404, 500)
- Instance-based configuration
- Debug mode support

## Prerequisites

- Python 3.7+
- SQL Server (optional, for database features)
- ODBC Driver 18 for SQL Server (if using database features)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Flask_Application
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Update the database configuration in `flaskr/__init__.py`:

```python
SQL_SERVER='localhost'  # Your SQL Server host
SQL_DATABASE='flaskr_db'  # Your database name
SQL_USERNAME='your_username'  # Your username
SQL_PASSWORD='your_password'  # Your password
```

Alternatively, create a `config.py` file in the `instance/` folder for environment-specific settings.

## Running the Application

### Development Mode

```bash
flask --app flaskr run --debug
```

The application will be available at `http://127.0.0.1:5000`

### Production Mode

```bash
flask --app flaskr run
```

## Project Structure

```
Flask_Application/
├── flaskr/
│   ├── __init__.py      # Application factory and configuration
│   └── db.py            # Database connection utilities
├── instance/            # Instance-specific files (gitignored)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## API Endpoints

- `GET /hello/` - Returns "Hello, World!" message

## Error Handling

The application includes custom error handlers for:
- 404 Not Found
- 500 Internal Server Error

## Dependencies

- Flask 3.1.2
- Werkzeug 3.1.4
- Jinja2 3.1.6
- pyodbc 5.2.0 (optional, for SQL Server)

See `requirements.txt` for complete list.

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]