import pytest
from flaskr import create_app, db


@pytest.fixture
def app():
    """Create and configure a new app instance for tests run inside Compose.

    Uses the Docker service hostnames (SQL Server available as `sqlserver`).
    """
    app = create_app({
        'TESTING': True,
        'SQL_DRIVER': 'ODBC Driver 18 for SQL Server',
        'SQL_SERVER': 'sqlserver',
        'SQL_DATABASE': 'flaskr_db',
        'SQL_USERNAME': 'sa',
        'SQL_PASSWORD': 'YourStrong@Passw0rd',
    })
    yield app


@pytest.fixture(autouse=True)
def clean_db(app):
    """Automatically clean the `banks` table before each test for isolation."""
    with app.app_context():
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute('DELETE FROM banks')
        conn.commit()
        cur.close()
    yield


@pytest.fixture
def client(app):
    return app.test_client()


def _latest_bank_id(app):
    with app.app_context():
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute('SELECT TOP 1 id FROM banks ORDER BY id DESC')
        row = cur.fetchone()
        cur.close()
        return row[0] if row else None


def create_bank(client, name, location):
    return client.post('/banks/add', data={'name': name, 'location': location}, follow_redirects=True)


def test_index_shows_empty_state(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'No Banks Found' in resp.data


def test_add_validation(client):
    # Missing name
    resp = client.post('/banks/add', data={'name': '', 'location': 'Loc'}, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Bank name and location are required' in resp.data


def test_create_and_detail_view(client, app):
    create_bank(client, 'Detail Bank', 'Detail Location')
    bank_id = _latest_bank_id(app)
    assert bank_id is not None

    resp = client.get(f'/banks/{bank_id}')
    assert resp.status_code == 200
    assert b'Detail Bank' in resp.data
    assert b'Detail Location' in resp.data
    assert b'Created At' in resp.data and b'Last Updated' in resp.data


def test_list_ordering(client, app):
    # Create two banks; later one should appear first (ORDER BY id DESC)
    create_bank(client, 'First Bank', 'L1')
    create_bank(client, 'Second Bank', 'L2')

    resp = client.get('/')
    assert resp.status_code == 200
    data = resp.data
    idx_first = data.find(b'First Bank')
    idx_second = data.find(b'Second Bank')
    assert idx_second != -1 and idx_first != -1
    assert idx_second < idx_first


def test_edit_validation(client, app):
    create_bank(client, 'ToEdit', 'Old')
    bank_id = _latest_bank_id(app)
    # Submit empty name
    resp = client.post(f'/banks/{bank_id}/edit', data={'name': '', 'location': ''}, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Bank name and location are required' in resp.data


def test_delete_nonexistent_shows_redirect(client):
    # Deleting non-existent id should redirect to index with flash
    resp = client.post('/banks/9999/delete', follow_redirects=True)
    assert resp.status_code == 200
    assert b'Bank not found' in resp.data