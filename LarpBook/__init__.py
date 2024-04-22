from flask import Flask

from config import Config
from LarpBook.extensions import db, login_manager, csrf, session, stripe

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    session.init_app(app)
    stripe.init_app(app)

    # Register blueprints here
    from LarpBook.Main import bp as main_bp
    app.register_blueprint(main_bp)

    from LarpBook.Auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from LarpBook.User import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    from LarpBook.Events import bp as events_bp
    app.register_blueprint(events_bp, url_prefix='/events')

    from LarpBook.Questions import bp as questions_bp
    app.register_blueprint(questions_bp, url_prefix='/questions')

    configure_jinja(app)

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app

def configure_jinja(app):
    @app.template_filter('currency')
    def currency_filter(value):
        return f"£{value:.2f}"