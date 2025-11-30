import pyodbc
from datetime import datetime

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        connection_string = (
            f"DRIVER={{{current_app.config['SQL_DRIVER']}}};"
            f"SERVER={current_app.config['SQL_SERVER']};"
            f"DATABASE={current_app.config['SQL_DATABASE']};"
            f"UID={current_app.config['SQL_USERNAME']};"
            f"PWD={current_app.config['SQL_PASSWORD']};"
        )
        g.db = pyodbc.connect(connection_string)
        g.db.autocommit = False

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()