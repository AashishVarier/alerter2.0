# Architecture
![Screenshot of the design.](/documentation/blog4_1.JPG)

# Modules:
- Synthetic Data : to generate data. It publishes raw data topic in Kafka.
- Incident Handling : to consume raw data topic and identify incidents from data available in elasticsearch DB. It will publish an alert topic to kafka.
- Kafka: pub/sub which act as buffer for generated data.
- Docker Compose: Used to simulate different servers and to ease the deployment of various services used in this project
- Elasticsearch and Logstash: Used as one of the consumer for raw data topic from kafka and as storage for the generated data.
- Anomaly Detection (pending) : uses fixed windowing of data and API error count as aggregation functions for real time data processing. And unsupervised learning using isolation forest for anomaly detection.
- Alerter (pending): at present it is implemented as a separate module mainly to act as event based alerts from alert topic consumed from kafka.

# How to run ?
- Docker should be installed. Use the below command to run the services.
```
docker-compose up
```
- Use the following endpoint to generate data:
> http://localhost:8080/data-gen/<number-of-entries>


Read more about it [here](https://variableduck.com/blog/blog4.html).





