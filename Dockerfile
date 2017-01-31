FROM python:3.5

MAINTAINER Spoqa
ENV PONG_PATH=""

RUN apt-get update && \
    apt-get install -y libcairo2 libpango1.0-0 libgdk-pixbuf2.0-0 \
                       shared-mime-info python3-cffi python3-lxml \
                       unzip otf-freefont ttf-freefont \
                       fonts-nanum fonts-nanum-extra fonts-nanum-coding \
                       ttf-baekmuk ttf-kochi-gothic ttf-kochi-mincho \
                       ttf-wqy-zenhei ttf-wqy-microhei && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /tmp
RUN wget https://github.com/spoqa/spoqa-han-sans/releases/download/1.0.0/SpoqaHanSans_all.zip && \
    unzip SpoqaHanSans_all.zip && \
    find SpoqaHanSans_all -name '*.ttf' -print0 | xargs -0 mv -t /usr/share/fonts/ && \
    fc-cache -f -v && \
    rm -rf __MACOSX SpoqaHanSans_all
WORKDIR /

COPY . /app
WORKDIR /app
RUN pip3 install -e .

EXPOSE 8080
CMD if [ "$PONG_PATH" = "" ]; then \
        html2pdfd; \
    else \
        html2pdfd --pong-path="$PONG_PATH"; \
    fi
