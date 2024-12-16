import datetime
import random

logList = []
baseMsg = "<102>Aug 04 {time_stamp} apic-prod-dc-mgmt-01.testAPI.co.in apimanagement[-]: {{\"status_code\":\"\\\"{status_code}\\\"\"}}"
statusCode = [
    "500 Internal Server Error",
    "404 Not Found",
    "403 Forbidden",
    "401 Unauthorized",
    "400 Bad Request",
    "200 OK"
]


#def data_gen(numEntry):
for i in range(2):
    logs =  {
    "host": "10.123.17.140",
    "@version": "1",
    "@timestamp": datetime.datetime.now().isoformat() + "Z",
    "port": 55000 + i ,
    "message":  baseMsg.format(time_stamp = datetime.datetime.now().isoformat() , status_code = random.choices(statusCode, weights=[5, 5, 5, 5, 5, 80], k =1)[0] ) ,
    "type": "apitcp"
  }
    logList.append(logs)

print(logList)