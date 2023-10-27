FROM python:3.11-slim-buster
WORKDIR /project

COPY . .

RUN python3.11 -m pip install --no-cache-dir --upgrade pip \
&& python3.11 -m pip install -U setuptools \
&& python3.11 -m pip install --no-cache-dir -r requirements.txt

CMD [ "python", "-u", "./ingest.py" ]