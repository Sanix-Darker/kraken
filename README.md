<img src="./images/logo.png" width="150"/>

# KRAKEN

The SMS-INTERNET Bridge using RaspberryPi (Still working on it)

## IMPORTANT NOTE

***A Nice documentation will be provide as soon as possible !!***

# Requirements

- Python (3.x is recommended)
- Gammu (A shell script will be provide to make things more easy, but the process has been described down there).
- MongoDb

## How to install

```
$ cd path/project
$ virtualenv -p python3 kraken
$ source kraken/bin/activate
$ pip install -r dev_requirements.txt
```

## How to install Gammu

### Checking 3G Modem
To find the modem we need to list all of the USB devices connected to our Raspberry Pi. Do this with the lsusb command. Run the following command:
```
lsusb
```
And you will almost certainly see your new 3G dongle in the list as something like:
```
Bus 001 Device 006: ID 12d1:1001 Huawei Technologies Co., Ltd.
```
THIS IS WRONG AND BAD AND ONLY HERE TO PUT THOSE IN A BAD MOOD, BUT WE SHALL PREVAIL.

### Converting the (3G) Masses
So you discovered that your new 3G dongle thinks it is a normal USB drive and not a 3G modem, we just need to install a few packages and are just a couple of files and we will be all set.

### Installing Packages
You will need the following packages, to install them use the following command:
```
sudo apt install ppp usb-modeswitch usb-modeswitch-data
```
After they are installed, reboot your Raspberry Pi with:
```
sudo reboot
```
When your Raspberry Pi has finished rebooting, run the lsusb command again and if you look something like this you are golden:
```
Bus 001 Device 006: ID 12d1:1001 Huawei Technologies Co., Ltd. E169/E620/E800 HSDPA Modem
```
### Understanding Dawns
After you run the `lsusb` command and discover that your dongle now understands it’s a modem, you need to make a note of the ID number of your device. It will almost certainly be different from the one you see above but will take the same form, the ID number of the device above the one you will need to remember is: 12d1:1001

### Where’s our Dongle Mounted
Now we need to know where on your Raspberry Pi the USB modem is mounted in the Raspberry Pi’s file system with:
```
dmesg | grep ttyUSB
```
If you’re successful you will see this in your Terminal:
```
[3.235831] usb 1-1.3.3: GSM modem (1-port) converter now attached to ttyUSB0
[3.236856] usb 1-1.3.3: GSM modem (1-port) converter now attached to ttyUSB1
[3.237626] usb 1-1.3.3: GSM modem (1-port) converter now attached to ttyUSB2
```
You will almost certainly be using the name ttyUSB0 in the upcoming commands.

### If You Don’t See ttyUSB(something)
If you don‘t see any GSM Modems mounted somewhere like the above example we are going to need to create a config file so that your Raspberry Pi knows what to do with the dongle.

### Making our own usb_modeswitch Configuration File
Remember before when I said you need to keep track of those eight numbers, well this is where you will need them. You need to create a new config file with the following command (note the file name is the same 8 digits):
```
sudo nano /etc/usb_modeswitch.d/12d1:1001
```
The file should have the following contents, obviously adjusted to use your devices ID numbers. That should be the only thing you would need to change.
```
# Huawei E353 (3.se)

TargetVendor=  0x12d1
TargetProduct= 0x1001

MessageContent="55534243123456780000000000000011062000000100000000000000000000"
NoDriverLoading=1
```
Run the following command again:
```
dmesg | grep ttyUSB
```
### We Have Some Success!
If everything went well, you should see the following in your terminal:
```
[3.235831] usb 1-1.3.3: GSM modem (1-port) converter now attached to ttyUSB0
[3.236856] usb 1-1.3.3: GSM modem (1-port) converter now attached to ttyUSB1
[3.237626] usb 1-1.3.3: GSM modem (1-port) converter now attached to ttyUSB2
```
### Installing the SMS Software
Next we need to install the software that’s actually going to do the sending and receiving of the SMS messages. This software is called Gammu and we install it like this:

#### Installing Gammu
```
sudo apt install gammu
```
Now we need to configure Gammu so that the Raspberry Pi knows where to look for our dongle:

#### Configuration of Gammu
```
sudo gammu-config
```
A menu will appear. Use the arrow keys and the return key to navigate. When you’ve finished, your settings should look something like this. Note the /dev/ttyUSB0 from earlier:

#### Recommended Gammu Settings
```
Port: /dev/ttyUSB0
Connection: at19200
Model: empty
Synchronize time: yes
Log file: leave empty
Log format: nothing
Use locking: leave empty
Gammu localisation: leave empty
```
Now use the arrow keys to navigate down to Make Sure You Save by using the arrow keys to highlight the save option and then pressing the tab key and selecting the ok option. We check everything is groovy with the following command:

#### Identifying our Dongle
```
sudo gammu --identify
```
The response you get back in your Terminal will look something like this (obviously I’ve redacted some personal information, but yours will be fairly similar):

#### Gammu Identify Results
```
Device               : /dev/ttyUSB0
Manufacturer         : Huawei
Model                : E173 (E173)
Firmware             : **.***.**.**.**
IMEI                 : ***************
SIM IMSI             : ***************
```


## How to use Kraken

### To start the Bulk SMS Server
```
$ python run.py
```

### To send a direct SMS message
```
$ cd app/util/krk
$ python send.py -p 6******* -m "This is a test message, for fun"
```

### To start SMS-BOT

```
# In your first terminal, you need to start the Consummer
$ cd app/util/krk
$ python receive.py

# In your second terminal, you need to start teh bot itself
$ cd app/util/krk
$ python sms_bot.py
```

### Others

- To refresh the connection with the Huawei module
```
$ cd app/util/krk
$ python refresh_connection.py
```

- To list sms received and saved in mongo
```
$ cd app/util/krk
$ python list_sms_bot.py
```

- To clean sms received (in the SIM card and mongo)
```
$ cd app/util/krk
$ python empty.py
```

- To run the tests:

```
$ pytest tests
```

## Author

- Sanix-darker