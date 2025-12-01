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
            f"TrustServerCertificate=yes;"
        )
        g.db = pyodbc.connect(connection_string)
        g.db.autocommit = False

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# Bank CRUD Operations

def get_all_banks():
    """Retrieve all banks from the database."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, name, location, created_at, updated_at FROM banks ORDER BY id DESC')
    banks = []
    for row in cursor.fetchall():
        banks.append({
            'id': row[0],
            'name': row[1],
            'location': row[2],
            'created_at': row[3],
            'updated_at': row[4]
        })
    cursor.close()
    return banks


def get_bank_by_id(bank_id):
    """Retrieve a single bank by ID."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, name, location, created_at, updated_at FROM banks WHERE id = ?', (bank_id,))
    row = cursor.fetchone()
    cursor.close()
    
    if row:
        return {
            'id': row[0],
            'name': row[1],
            'location': row[2],
            'created_at': row[3],
            'updated_at': row[4]
        }
    return None


def create_bank(name, location):
    """Create a new bank."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO banks (name, location) VALUES (?, ?)',
        (name, location)
    )
    db.commit()
    bank_id = cursor.execute('SELECT @@IDENTITY').fetchone()[0]
    cursor.close()
    return bank_id


def update_bank(bank_id, name, location):
    """Update an existing bank."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'UPDATE banks SET name = ?, location = ?, updated_at = GETDATE() WHERE id = ?',
        (name, location, bank_id)
    )
    db.commit()
    cursor.close()
    return cursor.rowcount > 0


def delete_bank(bank_id):
    """Delete a bank by ID."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM banks WHERE id = ?', (bank_id,))
    db.commit()
    cursor.close()
    return cursor.rowcount > 0