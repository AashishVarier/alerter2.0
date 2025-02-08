FROM python:3.9-slim

WORKDIR /app
COPY requirement.txt .
COPY . .

RUN pip install -r requirement.txt

EXPOSE 8081

CMD [ "python3", "anomaly.py" ]