FROM ubuntu:24.04

RUN apt-get update && apt-get install wget build-essential make cmake g++ gcc libwebsockets-dev libc-ares2 libc-ares-dev openssl uuid uuid-dev libcjson1 libcjson-dev -y
WORKDIR /usr/src

RUN wget http://mosquitto.org/files/source/mosquitto-2.0.20.tar.gz && tar xzvf mosquitto-2.0.20.tar.gz
RUN cd mosquitto-2.0.20 && make && make binary && make install
RUN groupadd mosquitto
RUN useradd -s /sbin/nologin mosquitto -g mosquitto -d /var/lib/mosquitto
RUN mkdir -p /etc/mosquitto/conf.d /run/mosquitto /var/log/mosquitto/ /var/lib/mosquitto/
RUN chown -R mosquitto:mosquitto /run/mosquitto
RUN chown -R mosquitto:mosquitto /etc/mosquitto/conf.d
RUN chown -R mosquitto:mosquitto /var/log/mosquitto/
RUN chown -R mosquitto:mosquitto /var/lib/mosquitto/
# RUN mv /etc/mosquitto/mosquitto.conf.example /etc/mosquitto/mosquitto.conf

ENTRYPOINT ["/usr/local/sbin/mosquitto", "-c", "/etc/mosquitto/mosquitto.conf"]