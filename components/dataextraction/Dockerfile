FROM laudio/pyodbc

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -y install gcc mono-mcs g++ git curl && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt


ADD dataextraction.py /app/dataextraction.py
RUN chmod +x /app/dataextraction.py


ENTRYPOINT ["python"]
CMD ["/app/dataextraction.py"]