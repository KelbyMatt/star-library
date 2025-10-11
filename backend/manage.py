from app.database import engine
from app.models import dbBase

print("Attempting to create database tables...")

dbBase.metadata.create_all(bind=engine)

print("Successfully created Database tables (if they didn't already exist).")