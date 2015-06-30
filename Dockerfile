FROM debian:jessie
MAINTAINER Michal Rostecki <michal.rostecki@gmail.com>

RUN apt-get update \
    && apt-get -y install \
        build-essential \
        git \
        python-dev \
        python-pip \
    && apt-get clean

ADD . /opt/obd-consumer

RUN pip install -e /opt/obd-consumer

COPY start.sh /

CMD ["/start.sh"]
