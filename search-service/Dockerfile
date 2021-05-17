FROM python:3.7

RUN apt-get update -y && \
    apt-get install -y python-pip python3.7-dev

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY script/server.sh ./

COPY src ./src

EXPOSE 8002

ENTRYPOINT ["./server.sh"]
