FROM python:3

RUN pip install json
RUN pip install python-dotenv

WORKDIR /ray-tracer

ENTRYPOINT [ "bash" ]