# users [ user_id, username, _date ]
from . import Model


class Sms(Model.Model):
    def __init__(self, json=None):
        super().__init__(json)
        if json is None:
            json = {"_id": "test"}
        self.json = json
        self.collection = self.database.get_db()["sms"]
        self.schema = {
            "type": "object",
            "required": ["s_number", "date", "encoding", "from_number", "message", "command"],
            "properties": {
                "s_number": {"type": "string"},
                "date": {"type": "string"},
                "encoding": {"type": "string"},
                "from_number": {"type": "string"},
                "message": {"type": "string"},
                "command": {"type": "object"}
            }
        }
