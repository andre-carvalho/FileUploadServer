# To build image for this dockerfile use this command:
#   docker build -t softwarevale/upload-server:v1 -f env/Dockerfile .
#
# To run without compose but with shell terminal use this command:
#   docker run -p 8181:8000 --name upload-server --rm -it softwarevale/upload-server:v1 sh
#
# To run without compose and without shell terminal use this command:
#   docker run -p 8181:8000 --name upload-server --rm -d softwarevale/upload-server:v1
#
#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM python:3.6-alpine

LABEL "br.com.softwarevale"="File Upload" \
br.com.softwarevale="microservice" \
version="0.1" \
author="Andre Carvalho" \
author.email="afacarvalho@yahoo.com.br" \
description="This microservice receive the binary files from \
app client and store them to disc."

ENV PYTHONUNBUFFERED 1
#-------------Application Specific Stuff ----------------------------------------------------

RUN apk update \
  && apk add --no-cache --update \
    build-base \
    postgresql \
    postgresql-dev \
    libpq \
    python-dev \
    py-pip \
    zlib-dev \
    tzdata

ENV TZ=America/Sao_Paulo

ENV LIBRARY_PATH=/lib:/usr/lib

ENV INSTALL_PATH /server

COPY api $INSTALL_PATH/api
COPY utils $INSTALL_PATH/utils

# Install Python requirements
RUN pip install -r $INSTALL_PATH/utils/requirements.txt

EXPOSE 8000

WORKDIR $INSTALL_PATH/api

# using the gunicorn as a WSGI server
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "wsgi:app"]
