# Author: Kazuki Sona
# Title : Dockerfile

FROM ubuntu:latest
MAINTAINER Kazuki Sona "kazukisona@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python3.6 python3-pip python3.6-dev build-essential
RUN apt-get install -y wget 

RUN apt-get -y install fontconfig libxrender-dev libxext-dev xfonts-base xfonts-75dpi libfreetype6 libpng-dev zlib1g-dev libjpeg-dev openssl libicu-dev

RUN wget https://downloads.wkhtmltopdf.org/0.12/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN tar -xJf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN cp wkhtmltox/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf
RUN cp wkhtmltox/bin/wkhtmltoimage /usr/local/bin/wkhtmltoimage 
RUN touch .wkhtmltopdf

# Add source files
RUN mkdir /app
RUN cd app
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app

ENTRYPOINT ["python3"]
CMD ["application.py"]
