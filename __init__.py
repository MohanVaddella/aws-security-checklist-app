from flask import Flask
import os

def create_app():
    
    app = Flask(__name__)
    
    
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),  
        DEBUG=True  
    )
    
    
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    
    @app.errorhandler(404)
    def page_not_found(e):
        return "Page not found!", 404

    return app
