from flask import Flask, jsonify, request, render_template
from db import get_db, close_db, init_db
from models import Workout, Exercise

import os

# Flask Application Setup

app = Flask(__name__)
app.config["DATABASE"] = "instance/workouts.db"


@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

# Routes
@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM workouts ORDER BY date DESC")
    rows = cursor.fetchall()

    workouts = [
        Workout(row["id"], row["date"], row["name"]).to_dict()
        for row in rows
    ]

    return render_template("index.html", workouts=workouts)

# View Workout Detail
@app.route("/workouts/<int:workout_id>/view")
def workout_view(workout_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM workouts WHERE id = ?", (workout_id,))
    workout_row = cursor.fetchone()

    if workout_row is None:
        return "Workout not found", 404

    cursor.execute("SELECT * FROM exercises WHERE workout_id = ?", (workout_id,))
    exercise_rows = cursor.fetchall()

    workout = Workout(
        workout_row["id"],
        workout_row["date"],
        workout_row["name"]
    ).to_dict()

    workout["exercises"] = [
        Exercise(
            row["id"],
            row["workout_id"],
            row["name"],
            row["sets"],
            row["reps"],
            row["weight"]
        ).to_dict()
        for row in exercise_rows
    ]

    return render_template("workout_detail.html", workout=workout)


# Workout Endpoints
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

# Update Workout
@app.route("/workouts/<int:workout_id>", methods=["PUT"])
def update_workout(workout_id):
    data = request.get_json()

    if not data or "date" not in data or "name" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE workouts SET date = ?, name = ? WHERE id = ?",
        (data["date"], data["name"], workout_id)
    )

    if cursor.rowcount == 0:
        return jsonify({"error": "Workout not found"}), 404

    db.commit()

    return jsonify({
        "id": workout_id,
        "date": data["date"],
        "name": data["name"]
    })

# Delete Workout
@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM exercises WHERE workout_id = ?",
        (workout_id,)
    )

    cursor.execute(
        "DELETE FROM workouts WHERE id = ?",
        (workout_id,)
    )

    if cursor.rowcount == 0:
        return jsonify({"error": "Workout not found"}), 404

    db.commit()
    return jsonify({"message": "Workout deleted"})

# Exercise Endpoints
@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()

    required_fields = ["workout_id", "name", "sets", "reps", "weight"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO exercises (workout_id, name, sets, reps, weight)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data["workout_id"],
            data["name"],
            data["sets"],
            data["reps"],
            data["weight"]
        )
    )

    db.commit()
    exercise_id = cursor.lastrowid

    exercise = Exercise(
        exercise_id,
        data["workout_id"],
        data["name"],
        data["sets"],
        data["reps"],
        data["weight"]
    )

    return jsonify(exercise.to_dict()), 201

# Fetch Workout Detail
@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout_detail(workout_id):
    db = get_db()
    cursor = db.cursor()

    # Fetch workout
    cursor.execute(
        "SELECT * FROM workouts WHERE id = ?",
        (workout_id,)
    )
    workout_row = cursor.fetchone()

    if workout_row is None:
        return jsonify({"error": "Workout not found"}), 404

    workout = Workout(
        workout_row["id"],
        workout_row["date"],
        workout_row["name"]
    ).to_dict()

    # Fetch exercises for workout
    cursor.execute(
        "SELECT * FROM exercises WHERE workout_id = ?",
        (workout_id,)
    )
    exercise_rows = cursor.fetchall()

    exercises = [
        Exercise(
            row["id"],
            row["workout_id"],
            row["name"],
            row["sets"],
            row["reps"],
            row["weight"]
        ).to_dict()
        for row in exercise_rows
    ]

    workout["exercises"] = exercises

    return jsonify(workout)


# Delete Exercise
@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM exercises WHERE id = ?",
        (exercise_id,)
    )

    if cursor.rowcount == 0:
        return jsonify({"error": "Exercise not found"}), 404

    db.commit()
    return jsonify({"message": "Exercise deleted"})


# Run app
if __name__ == "__main__":
    os.makedirs("instance", exist_ok=True)
    init_db()
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)

