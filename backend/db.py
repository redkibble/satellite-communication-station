import json
class AlertDatabase:
    def __init__(self):
        self.db = {}

    def add(self, key, value):
        self.db[key] = value

    def get(self, key):
        return self.db[key]

    def remove(self, key):
        del self.db[key]

    def __str__(self):
        return str(self.db)

class LocalDatabase(AlertDatabase):
    def __init__(self):
        super().__init__()
        self.filename = "alerts.json"

    def load(self):
        with open(self.filename, "r") as f:
            self.db = json.load(f)

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.db, f)