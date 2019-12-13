import json

from app.util.krk.send import send_sms
from app.util.krk.list_sms import get


class SmsPresentResources:
    def on_get(self, req, resp):
        resp.media = {
            "message": "Welcome to Kraken BulkSMS API!",
        }


class SmsResources:
    def on_get(self, req, resp, operation):
        try:
            if operation == "send" and bool(req.params):
                params = req.params
                if params["phone"] is not None and params["message"] is not None:
                    send_sms(params["phone"], params["message"])
                    resp.media = {
                        "status": "success",
                        "message": "Message sent successfully to {}, content {}!".format(params["phone"],
                                                                                         params["message"]),
                    }
                else:
                    resp.media = {
                        "status": "error",
                        "message": "Provide correct parameters!",
                    }
            elif operation == "list":
                results = json.loads(get("app/util/krk/inbox.json"))
                resp.media = {
                    "status": "success",
                    "result": results
                }
        except Exception as es:
            resp.media = {
                "status": "error",
                "message": "An internal server error occured!",
            }
            print(es)
