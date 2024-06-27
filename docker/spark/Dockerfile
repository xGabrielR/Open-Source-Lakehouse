FROM maven:3.3-jdk-8 AS mvn-build
WORKDIR /usr/src/spark/

COPY ./pom.xml .
RUN mvn clean dependency:copy-dependencies

FROM bitnami/spark:3.4.2 AS spark
USER root

RUN touch /opt/bitnami/spark/conf/hadoop-metrics2-s3a-file-system.properties

COPY --from=mvn-build /usr/src/spark/lib/* /opt/bitnami/spark/jars/
COPY spark-defaults.conf /opt/bitnami/spark/conf

RUN chmod u+x /opt/bitnami/spark/sbin/* && chmod u+x /opt/bitnami/spark/bin/*