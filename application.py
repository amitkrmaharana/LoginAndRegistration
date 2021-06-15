from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initializing as a global library
database = SQLAlchemy()
migrate = Migrate()


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    # Initialize Plugins
    database.init_app(app)
    migrate.init_app(app, database)
    with app.app_context():
        # Include our Routes
        import routes
        # Register Blueprints
        app.register_blueprint(routes.bp)

        return app
