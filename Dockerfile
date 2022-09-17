FROM python:3.8.6-buster

COPY . .

COPY requirements.txt /requirements.txt
COPY dataqc/abrolhos_qc.csv /abrolhos_qc.csv

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT