from models.Sms import Sms


def perform_fetch(find_request=None):
    """

    Args:
        find_request:

    Returns:

    """
    if find_request is None:
        find_request = Sms().findAll()

    try:
        list_sms = list(find_request)
        for row in list_sms:
            del row['_id']
        return list_sms
    except Exception as es:
        print(es)

    return []


def get_all():
    """

    Returns:

    """
    return perform_fetch()


def get_only_messages():
    """

    Returns:

    """
    return perform_fetch(Sms().findBy({"command.status": {"$exists": False}}))


def get_all_commands():
    """

    Returns:

    """
    return perform_fetch(Sms().findBy({"command.status": {"$exists": True}}))


def get_commands(pending=False):
    """
    Args:
        pending: At true it will return pending command
    Returns:
    """
    return perform_fetch(Sms().findBy({"command.status": pending}))


if __name__ == '__main__':
    print("[+] ------------")
    print("[+] get_all: ", get_all())
    print("[+] ------------")
    print("[+] get_only_messages: ", get_only_messages())
    print("[+] ------------")
    print("[+] get_all_commands(): ", get_all_commands())
    print("[+] ------------")
    print("[+] get_commands not executed yet : ", get_commands(False))
    print("[+] ------------")
    print("[+] get_commands allready executed : ", get_commands(True))
