import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQL_DRIVER='ODBC Driver 18 for SQL Server',
        SQL_SERVER='localhost',  # Update with your SQL Server host
        SQL_DATABASE='flaskr_db',  # Update with your database name
        SQL_USERNAME='your_username',  # Update with your username
        SQL_PASSWORD='your_password',  # Update with your password
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
    
    # a simple page that says hello
    @app.route('/hello/')
    def hello():
        return 'Hello, World!'
    
    # Register error handlers
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    # TODO: Will add the template files for errors later

    """Register error handlers."""
    
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        return render_template('errors/500.html'), 500