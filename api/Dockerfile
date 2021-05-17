FROM python:3.7

RUN apt-get update -y && \
    apt-get install -y python-pip python3.7-dev

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY requirements-dev.txt ./
RUN pip3 install -r requirements-dev.txt

COPY script/server.sh ./

COPY src ./src

EXPOSE 8001

ENTRYPOINT ["./server.sh"]
