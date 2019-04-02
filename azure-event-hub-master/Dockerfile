FROM python:3.6-slim
LABEL maintainer="Simen Jorgensen simen.jorgensen@sesam.io"


RUN pip install --upgrade pip

COPY ./service/requirements.txt /service/requirements.txt
RUN pip install -r /service/requirements.txt
COPY ./service /service

EXPOSE 5000

CMD ["python3", "-u", "./service/service.py"]
