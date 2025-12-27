document.addEventListener("DOMContentLoaded", () => {
    loadWorkouts();
    setupWorkoutForm();
    setupExerciseForm();
});

function loadWorkouts() {
    fetch("/workouts")
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("workout-list");
            if (!list) return;

            list.innerHTML = "";

            data.forEach(workout => {
                const li = document.createElement("li");

                li.innerHTML = `
                    <a href="/workouts/${workout.id}/view">
                        ${workout.name} (${workout.date})
                    </a>
                    <button onclick="deleteWorkout(${workout.id})">Delete</button>
                `;

                list.appendChild(li);
            });
        });
}

function setupWorkoutForm() {
    const form = document.getElementById("workout-form");
    if (!form) return;

    form.addEventListener("submit", event => {
        event.preventDefault();

        const date = document.getElementById("date").value;
        const name = document.getElementById("name").value;

        fetch("/workouts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ date, name })
        })
        .then(() => {
            form.reset();
            loadWorkouts();
        });
    });
}

function deleteWorkout(workoutId) {
    fetch(`/workouts/${workoutId}`, {
        method: "DELETE"
    })
    .then(() => loadWorkouts());
}

function setupExerciseForm() {
    const form = document.getElementById("exercise-form");
    if (!form) return;

    const workoutId = form.dataset.workoutId;

    form.addEventListener("submit", event => {
        event.preventDefault();

        const name = document.getElementById("exercise-name").value;
        const sets = document.getElementById("sets").value;
        const reps = document.getElementById("reps").value;
        const weight = document.getElementById("weight").value;

        fetch("/exercises", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                workout_id: workoutId,
                name,
                sets,
                reps,
                weight
            })
        })
        .then(() => location.reload());
    });
}

function deleteExercise(exerciseId) {
    fetch(`/exercises/${exerciseId}`, {
        method: "DELETE"
    })
    .then(() => location.reload());
}
