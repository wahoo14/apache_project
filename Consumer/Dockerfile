FROM apache/spark-py:v3.3.0

COPY . .

USER root

RUN apt-get update -y &&\
    apt-get install -y python3 &&\
    pip3 install -r requirements.txt

CMD ["python3", "-u", "consume.py"] 