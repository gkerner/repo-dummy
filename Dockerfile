FROM python:3.7.3-alpine

COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
EXPOSE 5555
COPY . /metrics_exporter
WORKDIR /metrics_exporter
CMD ["supervisord", "-c", "supervisor/supervisord.conf"]