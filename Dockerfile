FROM python:3

RUN pip install --requirement requirements.txt

WORKDIR /ray-tracer

ENTRYPOINT [ "bash" ]
