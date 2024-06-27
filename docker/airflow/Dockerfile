FROM python:3.10-slim
RUN apt-get update -y && apt-get upgrade -y

RUN pip install "apache-airflow==2.8.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.2/constraints-3.8.txt"
COPY ./requirements.txt ./tmp/requirements.txt
RUN pip install -r ./tmp/requirements.txt

COPY airflow.cfg /root/airflow/airflow.cfg

EXPOSE 8080
COPY ./entrypoint.sh /root

RUN chmod +x /root/entrypoint.sh
CMD ./root/entrypoint.sh