FROM python:3.10

RUN apt update && apt install -y socat

RUN pip install pycryptodome

COPY run.sh server.py /tmp/

RUN chmod +x /tmp/run.sh

USER 1000

ENTRYPOINT /tmp/run.sh
