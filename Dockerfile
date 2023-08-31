FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app/
RUN sed -i 's/\r$//g' /app/deployment/*
RUN chmod +x /app/deployment/*

ENTRYPOINT ["/app/deployment/entrypoint"]
