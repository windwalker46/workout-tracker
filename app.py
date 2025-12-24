from flask import Flask, jsonify
from db import get_db, close_db, init_db
import os

app = Flask(__name__)
app.config["DATABASE"] = "instance/workouts.db"


@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)


@app.route("/")
def health_check():
    return jsonify({"status": "Workout Tracker API running"})


if __name__ == "__main__":
    os.makedirs("instance", exist_ok=True)
    init_db()
    app.run(debug=True)
