FROM python:3.8-slim-bookworm

MAINTAINER Javier Perez de Frutos <javier.perezdefrutos@sintef.no>

# set language, format and stuff
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

WORKDIR /usr/src/website

RUN apt-get update
RUN apt-get install git -y
RUN pip install --upgrade pip
RUN pip install Flask==2.2.2
RUN pip install gdown==4.5.3
RUN pip install google-auth==1.35.0
RUN pip install google-auth-oauthlib==0.4.6
RUN pip install google-pasta==0.2.0
RUN pip install h5py==2.10.0
RUN pip install Jinja2==3.1.2
RUN pip install pytest==7.2.0
RUN pip install PyYAML==6.0
RUN pip install tqdm==4.62.2

COPY . WORKDIR

ENV PYTHONBUFFERED 1

ENTRYPOINT ["python", "./main.py"]