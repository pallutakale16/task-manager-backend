from flask_sqlalchemy import SQLAlchemy

# Single shared SQLAlchemy instance, imported by models and __init__.py
db = SQLAlchemy()