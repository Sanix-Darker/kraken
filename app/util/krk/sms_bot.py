# We fetch in mongod all command with the status as false
# We execute them and automatically pass them to true

from list_sms import get_commands
from search import search
from send import send_sms
from threading import Thread
import time


def chunks(s, n):
    """Produce `n`-character chunks from `s`."""
    for start in range(0, len(s), n):
        yield s[start:start + n]


def perform_command(phone, command, body):
    results, array_resp = "", []
    if "#search" in command.lower():
        results = search(body[:15], 2)

    for chunk in chunks(results, 130):
        send_sms(phone, chunk)


def command_job():
    while True:
        time.sleep(2)
        list_command = get_commands()
        if len(list_command) > 0:
            for command in get_commands():
                Thread(target=perform_command,
                       args=(command["from_number"],
                             command["label"],
                             command["body"],)).start()


if __name__ == '__main__':
    command_job()
