FROM python:3.12-slim

ENV SQS_QUEUE_P1=""
ENV SQS_QUEUE_P2=""
ENV SQS_QUEUE_P3=""
ENV AWS_REGION=""
ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""


WORKDIR /frontend_microservice_application
COPY . /frontend_microservice_application
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "--bind","0.0.0.0:8000", "main:app"]
