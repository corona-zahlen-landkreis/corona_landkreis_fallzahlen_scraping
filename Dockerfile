FROM python:3

RUN apt-get update && apt-get install -y sudo vim git locales locales-all less
RUN pip3 install bs4 requests cachecontrol[filecache] lockfile
RUN adduser python
RUN echo "python ALL=(ALL) NOPASSWD: ALL" >  /etc/sudoers.d/python


VOLUME /source
VOLUME /build

USER python
RUN /bin/bash -i
