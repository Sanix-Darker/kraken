from receive import erase_all_sms
from models.Sms import Sms

Sms().delete({})
print(erase_all_sms())