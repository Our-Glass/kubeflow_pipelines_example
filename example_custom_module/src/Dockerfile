FROM python:3.7
COPY . /usr/local/src/kfp/components/src
WORKDIR  /usr/local/src/kfp/components
COPY requirements.txt .
RUN pip install -r requirements.txt
