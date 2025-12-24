import sqlite3
from flask import g

DATABASE = "instance/workouts.db"


def get_db():
    """
    Opens a new database connection if one does not exist
    for the current application context.
    """
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """
    Closes the database connection at the end of the request.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """
    Initializes database tables.
    """
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            name TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            sets INTEGER NOT NULL,
            reps INTEGER NOT NULL,
            weight REAL NOT NULL,
            FOREIGN KEY (workout_id) REFERENCES workouts (id)
        );
    """)

    db.commit()
    db.close()
