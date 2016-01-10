FROM centos:7
MAINTAINER Michal Rostecki <michal.rostecki@gmail.com>

RUN yum -y install \
        epel-release \
        gcc \
        git \
        python-devel \
        sudo \
    && yum clean all

RUN yum -y install \
        python-virtualenv \
    && yum clean all

COPY obd_consumer_sudoers /etc/sudoers.d/obd_consumer_sudoers
ADD . /opt/obd-consumer

RUN mkdir -p /var/lib/obd-consumer/venv \
    && useradd --user-group obd \
    && chown -R obd: /opt/obd-consumer /var/lib/obd-consumer/venv

USER obd

RUN virtualenv /var/lib/obd-consumer/venv

RUN /var/lib/obd-consumer/venv/bin/pip install -e /opt/obd-consumer

COPY start.sh /

CMD ["/start.sh"]
