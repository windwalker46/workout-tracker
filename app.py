from flask import Flask, jsonify, request
from db import get_db, close_db, init_db
from models import Workout
import os

app = Flask(__name__)
app.config["DATABASE"] = "instance/workouts.db"


@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)


@app.route("/")
def health_check():
    return jsonify({"status": "Workout Tracker API running"})

@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()

    if not data or "date" not in data or "name" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO workouts (date, name) VALUES (?, ?)",
        (data["date"], data["name"])
    )

    db.commit()
    workout_id = cursor.lastrowid

    workout = Workout(workout_id, data["date"], data["name"])
    return jsonify(workout.to_dict()), 201

@app.route("/workouts", methods=["GET"])
def get_workouts():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM workouts ORDER BY date DESC")
    rows = cursor.fetchall()

    workouts = [
        Workout(row["id"], row["date"], row["name"]).to_dict()
        for row in rows
    ]

    return jsonify(workouts)




if __name__ == "__main__":
    os.makedirs("instance", exist_ok=True)
    init_db()
    app.run(debug=True)
