"""
A simple utility script to set up the database.
Run this once before starting the app for the first time.
"""


from app.database import engine
from app.models import dbBase

print("Attempting to create database tables...")

# Line reads the table definitions from models.py and creates them.
dbBase.metadata.create_all(bind=engine)

print("Successfully created Database tables (if they didn't already exist).")