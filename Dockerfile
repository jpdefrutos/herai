FROM python:3.8-slim-bookworm
RUN apt-get update
RUN apt-get install git -y
RUN mkdir /usr/src/mia_showroom
WORKDIR /usr/src/mia_showroom
RUN git clone https://github.com/jpdefrutos/herai .
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
ENV PYTHONBUFFERED 1