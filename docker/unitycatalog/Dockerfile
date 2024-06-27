FROM ubuntu:22.04
WORKDIR unitycatalog
USER root

RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install git -y && \
    apt-get install curl -y

RUN git clone https://github.com/unitycatalog/unitycatalog.git .

CMD [ "/unitycatalog/bin/start-uc-server" ]