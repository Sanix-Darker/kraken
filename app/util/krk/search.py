from subprocess import Popen, PIPE, STDOUT
import argparse


def search(text, count):
    cmd = './ext/googler --count ' + str(count) + ' --exact "' + text[1:] + '"'
    ping = Popen(cmd.split(" "), stdout=PIPE, stderr=PIPE)

    stdout, stderr = ping.communicate()
    return stdout.decode("utf-8")


if __name__ == '__main__':
    # Initialize the arguments
    # Example test : python search.py -t "python sucks" -c 3
    prs = argparse.ArgumentParser()
    prs.add_argument('-t', '--text', help='The text message', type=str, required=True)
    prs.add_argument('-c', '--count', help='The message you want to send in SMS', type=int, default=1)
    prs = prs.parse_args()

    print(search(prs.text, prs.count))
