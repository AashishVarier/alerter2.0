from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from confluent_kafka import Producer
import datetime

import os
import logging
import json
from time import sleep

HOST = os.getenv('ELASTIC', 'elasticsearch')
PORT=os.getenv('PORT', '9200')
SLEEP = os.getenv('SLEEP', '299')
es_conn = f"http://{HOST}:{PORT}"
logging.debug("es_conn - ", es_conn)

es =  Elasticsearch(es_conn)


def kafka_delivery_repot(err, msg):
    if err is not None:
        print(f"inc delivery failed : {err}")
    else:
        print(f"inc delivery sucess : {msg}")

def get_data_from_es ():
    response = None
    query = {
    "query" : {
    "range": {
      "@timestamp": {
        "gte": "now-5m/m",
        "lte": "now/m"
      }
    }
  },
    "_source" : [ "message" ]
            }
    try:
        rel = scan(
                client = es,
                query = query,
                index = 'kafka_logs',
                raise_on_error=True
            )
        logging.debug("rel - ", rel)
        result = list(rel)
        temp = []

        for hit in result:
            temp.append(hit['_source'])
        
        #print(temp)
        if len(temp) > 0:
          response = process_inc(temp)
        else:
          return f"Something Went wrong"
        
        return response
    except Exception as e:
      logging.warning(f"something went wrong in getDataFromEs - {e}")
      return f"Something Went wrong - {e}"

def process_inc (data):
  print(data)
  errorStatusCode = [
      "500 Internal Server Error",
      "404 Not Found",
      "403 Forbidden",
      "401 Unauthorized",
      "400 Bad Request"
  ]
  threshold = os.getenv('THRESHOLD', '0.5')

    #kafka config
  conf = {'bootstrap.servers':  os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')}
  producer = Producer(conf)


  #process dataframe

  #count = sum(errorSC in errorStatusCode for errorSC in data )
  total_errors = 0
  for errorSC in errorStatusCode:
    count = sum(errorSC in msg['message'] for msg in data )
    print(f"'{errorSC}' found {count} times")
    total_errors += count

  errorRatio = total_errors / (len(data))
  print(f"errorRatio - {errorRatio}")
  
  time = datetime.datetime.now().isoformat()
  
  if errorRatio > float(threshold):
    message = f'error ratio - {errorRatio} for data processed at- {time}. ErrorCount - {count}. Total count - {len(data)}'
    try:
      producer.produce('alert_data', key='inc_alert_data', value = message, callback=kafka_delivery_repot )

    except Exception as e:
      logging.warning(f"something went wrong in data_gen - {e}")
      return f"failed in creation of alert topic - {e}"
  
    finally:
    #ensures all message are delivered
      producer.flush()
      return "success in creation of alert topic"
    
  return f"error ratio within threshold of {threshold} found in the time - {time}"




#logger config
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
logging.debug("inc start")
print("inc start")

while True:
    print("inc loop")
    logging.debug("in loop de")
    result = get_data_from_es()

    print(result)
    sleep(int(SLEEP)) #to run every x seconds


