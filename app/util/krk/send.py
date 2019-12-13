from os import system as ss
import argparse


def send_sms(phone, message):
    print("[+] Sender PHONE:{}, MESSAGE:{}".format(phone, message))
    ss("echo '{}' | sudo gammu sendsms TEXT {}".format(message, phone))


if __name__ == '__main__':
    # Initialize the arguments
    # Example test : python send.py -p 6******* -m "This is a test message, for fun"
    prs = argparse.ArgumentParser()
    prs.add_argument('-p', '--phone', help='The phone number', type=str, required=True)
    prs.add_argument('-m', '--message', help='The message you want to send in SMS', type=str, required=True)
    prs.add_argument('-i', '--iteration', help='The number of time you want to send this message', type=int, default=1)
    prs = prs.parse_args()

    for i in range(prs.iteration):
        send_sms(prs.phone, prs.message)