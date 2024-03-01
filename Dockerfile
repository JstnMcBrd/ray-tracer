FROM python:3

COPY requirements.txt ./
RUN pip install --requirement requirements.txt

WORKDIR /ray-tracer

ENTRYPOINT [ "bash" ]
