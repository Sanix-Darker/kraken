from subprocess import Popen, PIPE, STDOUT
from os import system as ss
import argparse


def exec_command(command, output_file):
    ss(command + ' > ' + output_file)

    with open(output_file, "r") as fout:
        response = fout.read()

    return response


def search(text, count):
    return exec_command('./ext/googler --count ' + str(count) + ' --exact "' + text[1:] + '"', 'outt3.txt')


def wikki(text):
    return exec_command('wikipedia ' + text, 'outt2.txt')


if __name__ == '__main__':
    # Initialize the arguments
    # Example test : python search.py -t "python sucks" -c 3
    prs = argparse.ArgumentParser()
    prs.add_argument('-t', '--text', help='The text message', type=str, required=True)
    prs.add_argument('-c', '--count', help='The message you want to send in SMS', type=int, default=1)
    prs = prs.parse_args()

    print("search: ", search(prs.text, prs.count))
    print("wikki: ", wikki(prs.text))
