from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import pandas as pd

import os
import logging
import json
from time import sleep

HOST = os.getenv('ELASTIC', 'elasticsearch')
PORT=os.getenv('PORT', '9200')

es =  Elasticsearch(f"http://{HOST}:{PORT}")

def get_data_from_es ():

    query = {
    "query" : {
    "range": {
      "@timestamp": {
        "gte": "now-5m/m",
        "lte": "now/m"
      }
    }
  },
    "_source" : [ "@timestamp", "message" ]
            }
    try:
        rel = scan(
                client = es,
                query = query,
                index = 'kafka_logs',
                raise_on_error=True
            )

        result = list(rel)
        temp = []

        for hit in result:
            temp.append(hit['_source'])
            
        df= pd.DataFrame(temp)
        logging.info("completed getDataFromEs")
        
        return df
    except Exception as e:
      logging.warning(f"something went wrong in getDataFromEs - {e}")
      return f"Something Went wrong - {e}"

#logger config
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
logging.info("inc start")

while True:
    response = get_data_from_es()
    print(response)

    sleep(10) #to run every x seconds


