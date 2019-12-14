import time
from subprocess import Popen, PIPE, STDOUT
from models.Sms import Sms
from hashlib import md5
from threading import Thread

# Global command
GET_ALL_SMS_COMMAND = 'sudo gammu getallsms'
DELETE_ALL_SMS_COMMAND = 'sudo gammu deleteallsms'
ARRAY_FOLDER_LIST = [1]  # stand for inBox for the SIM and Inbox for he Phone, [1, 3] to clean everywhere
ARRAY_FOLDER_DELETE = [1, 3]  # stand for inBox for the SIM and Inbox for he Phone, [1, 3] to clean everywhere


def extract_command_from_message(message):
    """
    Args:
        message:
    Returns:
    """
    command = {}
    # We build our command object
    if "#" in message:
        command_status = False
        command_label = message.split(" ")[0]
        command_body = message.replace(message.split(" ")[0]+" ", "")
        command = {
            "status": command_status,
            "label": command_label,
            "body": command_body
        }
    return command


def extract_params_from_output(output):
    """
    Args:
        output:
    Returns:
    """
    output_array = output.split(": ")  # Notice the : and the space if not, it will not work properly

    s_number = output_array[1].split("\n")[0].replace('"', '')
    date = output_array[2].split("\n")[0]
    coding = output_array[3].split("\n")[0]
    remote_number = output_array[4].split("\n")[0].replace('"', '')
    message = output_array[5].split("\n\n")[1]
    command = extract_command_from_message(message)

    return {"s_number": s_number,
            "date": date,
            "encoding": coding,
            "from_number": remote_number,
            "message": message,
            "command": command}


def output_parser_to_json(output_first):
    """
    Args:
        output_first:
    Returns:
    """
    outputs = output_first.split("Location ")
    json_array = []
    if len(outputs) > 1:
        for output in outputs:
            if len(output) > 3:
                json_array.append(extract_params_from_output(output))
    return json_array


def exec_command(command):
    """
    Args:
        command:
    Returns:
    """
    proc = Popen(command, stdout=PIPE, stderr=STDOUT)
    return proc.communicate()[0].decode('utf-8')


def loop_through_folder(command, operation="list"):
    """
    Args:
        command:
        operation:
    Returns:
    """
    output, command_array = "", ""
    if operation == "delete":
        for i in ARRAY_FOLDER_DELETE:
            command_array = (command + " " + str(i)).split(" ")
    elif operation == "list":
        for i in ARRAY_FOLDER_LIST:
            command_array = (command + " " + str(i)).split(" ")

    output += exec_command(command_array)

    return output


def erase_all_sms():
    """
    Returns:
    """
    print("[+] Erasing all inbox messages list...")
    return loop_through_folder(DELETE_ALL_SMS_COMMAND, operation="delete")


def get_all_sms():
    """
    Returns:
    """
    return loop_through_folder(GET_ALL_SMS_COMMAND, operation="list")


def save_json_sms(json_sms):
    """
    Args:
        json_sms:
    Returns:
    """
    sms_fetch = list(Sms().findBy({
        "from_number": json_sms["from_number"],
        "message": json_sms["message"],
        "date": json_sms["date"]
    }))
    if len(sms_fetch) == 0:
        print("{+} Saving json_sms: ", json_sms)
        new_sms = Sms(json_sms)
        new_sms.save()


def receive_process():
    """
    Returns:
    """
    print("[+] Kraken receiver Started...")
    precedent_output = "-"
    while True:
        time.sleep(0.5)
        output = get_all_sms().replace("SMS sequences", "").replace("SMS parts in", "")
        md5_output = md5(output.encode()).hexdigest()
        md5_precedent_output = md5(precedent_output.encode()).hexdigest()
        if md5_output != md5_precedent_output:
            for json_sms in output_parser_to_json(output):
                save_json_sms(json_sms)
            precedent_output = output
            # The erase is to much sensible, will handle it later
            # out = erase_all_sms()


if __name__ == '__main__':
    Thread(target=receive_process).start()
