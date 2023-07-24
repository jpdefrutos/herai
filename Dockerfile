FROM python:3.8-slim-bookworm
RUN apt-get update
RUN apt-get install git -y
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
ENV PYTHONBUFFERED 1