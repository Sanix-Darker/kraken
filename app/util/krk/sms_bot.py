# We fetch in mongod all command with the status as false
# We execute them and automatically pass them to true

from list_sms_bot import get_commands
from search import search, wikki
from send import try_send_sms
from models.Sms import Sms
from threading import Thread
import time

ALLOWED_COMMAND = ["#search"]


def string_divide(string, div):
    l = []
    for i in range(0, len(string), div):
        l.append(string[i:i + div])
    return l


def perform_command(to_update, phone, command, body):
    results, array_resp, to_search = "", [], body[:25]
    if command.lower() in ALLOWED_COMMAND:
        if "#google" in command.lower():
            print("[+] Search for :", to_search)
            results = search(to_search, 3)

        if "#wiki" in command.lower():
            print("[+] Wikipedia for :", to_search)
            results = wikki(to_search)

        print("[+] results: ", results)
        if len(results) > 5:
            chunks = string_divide(results, 200)
            for chunk in chunks:
                print("[+] Sending :", chunk)
                try_send_sms(phone, chunk)
        else:
            try_send_sms(phone, "Any relevant results, try another search !")
            print("[+] Any relevant results, try another search !")

        print("[+]Update Made in the database !")

        to_update["command"]["status"] = True
        print("to_update:", to_update)
        Sms().update({
            "from_number": phone,
            "command.label": command,
            "command.body": body
        }, to_update)




def command_job():
    while True:
        time.sleep(2)
        list_command = get_commands()
        if len(list_command) > 0:
            for sms in list_command:
                command = sms["command"]
                perform_command(sms, sms["from_number"], command["label"], command["body"])


if __name__ == '__main__':
    print("[+] Kraken sms-bot started...")
    command_job()
