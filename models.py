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
