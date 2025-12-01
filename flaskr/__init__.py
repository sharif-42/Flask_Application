import os

from flask import Flask, render_template, request, redirect, url_for, flash

def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQL_DRIVER=os.environ.get('SQL_DRIVER', 'ODBC Driver 18 for SQL Server'),
        SQL_SERVER=os.environ.get('SQL_SERVER', 'localhost'),
        SQL_DATABASE=os.environ.get('SQL_DATABASE', 'flaskr_db'),
        SQL_USERNAME=os.environ.get('SQL_USERNAME', 'sa'),
        SQL_PASSWORD=os.environ.get('SQL_PASSWORD', 'YourStrong@Passw0rd'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Import database functions
    from . import db
    
    # Register teardown function
    app.teardown_appcontext(db.close_db)
    
    # Routes
    
    @app.route('/')
    def index():
        """Display list of all banks."""
        banks = db.get_all_banks()
        return render_template('index.html', banks=banks)
    
    @app.route('/banks/add', methods=['GET', 'POST'])
    def add_bank():
        """Add a new bank."""
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            location = request.form.get('location', '').strip()
            
            if not name or not location:
                flash('Bank name and location are required!', 'error')
                return render_template('add_bank.html')
            
            try:
                db.create_bank(name, location)
                flash(f'Bank "{name}" added successfully!', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error adding bank: {str(e)}', 'error')
                return render_template('add_bank.html')
        
        return render_template('add_bank.html')
    
    @app.route('/banks/<int:bank_id>')
    def bank_detail(bank_id):
        """Display details for a specific bank."""
        bank = db.get_bank_by_id(bank_id)
        if not bank:
            flash('Bank not found!', 'error')
            return redirect(url_for('index'))
        return render_template('bank_detail.html', bank=bank)
    
    @app.route('/banks/<int:bank_id>/edit', methods=['GET', 'POST'])
    def edit_bank(bank_id):
        """Edit an existing bank."""
        bank = db.get_bank_by_id(bank_id)
        if not bank:
            flash('Bank not found!', 'error')
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            location = request.form.get('location', '').strip()
            
            if not name or not location:
                flash('Bank name and location are required!', 'error')
                return render_template('edit_bank.html', bank=bank)
            
            try:
                db.update_bank(bank_id, name, location)
                flash(f'Bank "{name}" updated successfully!', 'success')
                return redirect(url_for('bank_detail', bank_id=bank_id))
            except Exception as e:
                flash(f'Error updating bank: {str(e)}', 'error')
                return render_template('edit_bank.html', bank=bank)
        
        return render_template('edit_bank.html', bank=bank)
    
    @app.route('/banks/<int:bank_id>/delete', methods=['POST'])
    def delete_bank(bank_id):
        """Delete a bank."""
        bank = db.get_bank_by_id(bank_id)
        if not bank:
            flash('Bank not found!', 'error')
            return redirect(url_for('index'))
        
        try:
            db.delete_bank(bank_id)
            flash(f'Bank "{bank.get("name")}" deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error deleting bank: {str(e)}', 'error')
        
        return redirect(url_for('index'))
    
    # Register error handlers
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    """Register error handlers."""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500