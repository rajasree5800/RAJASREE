import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import requests
#Provide your IBM Watson Device Credentials
organization = "8yp7tr"
deviceType ="rasp"

deviceId = "12345"
authMethod = "token"
authToken = "123456789"


def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)#Commands
        

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        
        slot1=random.randint(0, 200)
        #print(slot1)
        slot2 =random.randint(0, 200)
        #Send availabilty of slot1 & slot2 area of parking to IBM Watson
        data = { 'slot1' : slot1, 'slot2': slot2}
        #print (data)
        
        def myOnPublishCallback():
            print ("Published availabilty of slot1 = %s C" % slot1, "slot2 = %s %%" % slot2, "to IBM Watson")
            

        success = deviceCli.publishEvent("Parking", "json", data, qos=0, on_publish=myOnPublishCallback)
        if(slot1>=51):
                r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=WDxqL3Yf3gWocizB51pWW8kTMmsL37oekGBRPqIoiZr6WJiLcHkao6BO4jM8&sender_id=FSTSMS&message=SLOT1 IS FULL.....PLEASE WAIT FOR SOMETIME UNTIL THE SLOT GETS EMPTY...&language=english&route=p&numbers=8555097962')
                print(r.status_code)
        if(slot2>=51):
                r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=WDxqL3Yf3gWocizB51pWW8kTMmsL37oekGBRPqIoiZr6WJiLcHkao6BO4jM8&sender_id=FSTSMS&message=SLOT2 IS FULL.....PLEASE WAIT FOR SOMETIME UNTIL THE SLOT GETS EMPTY...&language=english&route=p&numbers=8555097962
                                 ')
                print(r.status_code)
                
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
