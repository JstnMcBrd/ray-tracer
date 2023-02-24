FROM python:3

RUN pip install numpy
RUN pip install python-dotenv

WORKDIR /ray-tracer

ENTRYPOINT [ "bash" ]
