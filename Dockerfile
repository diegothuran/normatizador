FROM ubuntu:16.04

MAINTAINER Carlos Quixada

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python python-pip
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.6 python3-pip
#RUN apt-get install libmysqlclient-dev

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN mkdir logs

RUN python3 -m nltk.downloader wordnet pros_cons reuters stopwords rslp punkt

ENTRYPOINT ["/docker-entrypoint.sh"]
