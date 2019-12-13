from models.Sms import Sms


def get():
    try:
        list_sms = list(Sms().findAll())
        for row in list_sms:
            del row['_id']

        return list_sms
    except Exception as es:
        print(es)

    return []
