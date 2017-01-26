FROM python:3.4

MAINTAINER Spoqa
ENV PONG_PATH=""

RUN apt-get update && \
    apt-get install -y libcairo2 libpango1.0-0 libgdk-pixbuf2.0-0 \
                       shared-mime-info python3-cffi python3-lxml && \
    rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app
RUN pip3 install -e .

EXPOSE 8080
CMD if [ "$PONG_PATH" = "" ]; then \
        html2pdfd; \
    else \
        html2pdfd --pong-path="$PONG_PATH"; \
    fi
