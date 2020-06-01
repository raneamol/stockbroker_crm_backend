from app import create_app

from waitress import serve

application = create_app()
serve(application)