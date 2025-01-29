FROM python:3.9-slim

WORKDIR /app
COPY requirement.txt .
COPY . .

RUN pip install -r requirement.txt

EXPOSE 8080
CMD [ "python", "synthetic_data_gen.py" ]