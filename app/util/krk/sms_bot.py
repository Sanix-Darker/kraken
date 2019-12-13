# We fetch in mongod all command with the status as false
# We execute them and automatically pass them to true

from list_sms import getAll

sms_list = getAll()

print("sms_list: ", sms_list)
