from confluent_kafka import Producer
from flask import Flask
import datetime
import random
import logging
import time
import os
import json

app = Flask(__name__)

def kafka_delivery_repot(err, msg):
    if err is not None:
        print(f"delivery failed : {err}")
    else:
        print(f"delivery sucess : {msg}")

@app.route("/")
def hello_world():
    return "<p>Hi ?</p>"

@app.get('/data-gen/<int:numEntry>')
def data_gen(numEntry):
  #kafka config
  conf = {'bootstrap.servers':  os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')}
  producer = Producer(conf)

  #data streaming
    
  baseMsg = "<102>MM - DD {time_stamp} apic-prod-dc-mgmt-01.testAPI.co.in apimanagement[-]: {{\"status_code\":\"\\\"{status_code}\\\"\"}}"
  statusCode = [
      "500 Internal Server Error",
      "404 Not Found",
      "403 Forbidden",
      "401 Unauthorized",
      "400 Bad Request",
      "200 OK"
  ]
  logging.info(f"in data_gen with parameter {numEntry}")
  try:
    for i in range(numEntry):
        logs =  {
          "host": f"10.123.17.{random.randint(1, 4)}",
          "@version": "1",
          "@timestamp": datetime.datetime.now().isoformat() + "Z",
          "port": 55000 + i ,
          "message":  baseMsg.format(time_stamp = datetime.datetime.now().isoformat() , status_code = random.choices(statusCode, weights=[20, 5, 5, 5, 5, 60], k =1)[0] ) ,
          "type": "apitcp"
        }
        producer.produce('raw_data_topic', key=str(i), value = json.dumps(logs), callback=kafka_delivery_repot )

        # poll to handle delivery report
        producer.poll(0)
        
        #simulating delay for log generation
        time.sleep(1)

    logging.info( f"{numEntry} data generated succsfully")
  
  except Exception as e:
      logging.warning(f"something went wrong in data_gen - {e}")
  
  finally:
      #ensures all message are delivered
      producer.flush()
      return f"data_gen with parameter {numEntry}"

if __name__ == '__main__':
    #flask config
    app.run(host='0.0.0.0', port='8080')

    #logger config
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    logging.info("synthetic_data_gen start")

   