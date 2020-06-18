#   This Dockerfile is intended to be used as development environment
#   for the "corona landkreis fallzahlen scraping" project:
#
#   https://github.com/corona-zahlen-landkreis/corona_landkreis_fallzahlen_scraping/
#
#
#   Basically, it preinstalls all dependencies and mounts the
#   source code to /landkreise.
#
#   Additionally, a new user is created with prefined UID/GID
#   matching the host user UID/GID in order to preserve file
#   ownership informations. 
#   (see: https://github.com/moby/moby/issues/2259)

FROM python:3

# UID & GID of host user
ARG UID=1000
ARG GID=1000

RUN apt-get update && apt-get install --yes vim nano locales locales-all less


# - new user with predefined GID/UID to preservice file ownership
RUN groupadd --gid ${GID} corona && useradd --create-home --uid ${UID} --gid ${GID} corona
USER corona

# - source code location
VOLUME /landkreise
# - add ~/.local/bin for pip --user
ENV PATH="/home/corona/.local/bin:${PATH}"
# - install dependencies
ADD requirements.txt /tmp/
RUN pip3 install --user --requirement /tmp/requirements.txt

CMD bash
