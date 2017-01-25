FROM python:3.4

MAINTAINER Spoqa

RUN apt-get update && \
    apt-get install -y libcairo2 libpango1.0-0 libgdk-pixbuf2.0-0 \
                       shared-mime-info python3-cffi python3-lxml && \
    rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app
RUN pip3 install -e .

EXPOSE 8080
CMD html2pdfd --port=8080
