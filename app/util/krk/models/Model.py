from . import Database
from jsonschema import validate, ValidationError


class Model:
    def __init__(self, json=None):
        if json is None:
            json = {"_id": "test"}
        self.json = json
        self.database = Database
        self.collection = self.database.get_db()["bonds"]
        self.schema = {}

    def save(self):
        if self.validate_input(self.json)[0]:
            self.collection.insert(self.json)
        else:
            print("[+] JSON not valid for save()")

    def update(self, param, json):
        if self.validate_input(json)[0]:
            self.collection.update_one(param, json)
        else:
            print("[+] JSON not valid for update()")

    def delete(self, param):
        self.collection.delete_many(param)

    def count(self, param):
        return self.collection.find(param).count()

    def findBy(self, param):
        return self.collection.find(param)

    def findAll(self):
        return self.collection.find()

    def close(self):
        self.collection.close()

    def validate_input(self, data):
        try:
            validate(data, self.schema)
            return True, ""
        except ValidationError as e:
            return False, str(e)
