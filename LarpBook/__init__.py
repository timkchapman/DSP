from flask import Flask

from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here

    # Register blueprints here
    from LarpBook.Main import bp as main_bp
    app.register_blueprint(main_bp)

    from LarpBook.Events import bp as events_bp
    app.register_blueprint(events_bp)

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app