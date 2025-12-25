class Workout:
    def __init__(self, id, date, name):
        self.id = id
        self.date = date
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "name": self.name
        }

class Exercise:
    def __init__(self, id, workout_id, name, sets, reps, weight):
        self.id = id
        self.workout_id = workout_id
        self.name = name
        self.sets = sets
        self.reps = reps
        self.weight = weight

    def to_dict(self):
        return {
            "id": self.id,
            "workout_id": self.workout_id,
            "name": self.name,
            "sets": self.sets,
            "reps": self.reps,
            "weight": self.weight
        }
