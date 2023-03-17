FROM python:3

RUN pip install pylint

RUN pip install numpy
RUN pip install python-dotenv
RUN pip install tqdm

WORKDIR /ray-tracer

ENTRYPOINT [ "bash" ]
