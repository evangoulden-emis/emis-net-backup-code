FROM python:slim-bookworm

WORKDIR /workspaces

ENV LANG=en_US.UTF-8
ENV PIPENV_VENV_IN_PROJECT=1

ARG USER=netauto

COPY ../requirements.txt /tmp

USER root

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update \
    && apt install -y --no-install-recommends sudo \
    git \
    vim \
    curl \
    cron \
    && apt install -y python3.11 \
    && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --upgrade pip \
    && useradd -ms /bin/bash $USER \
    && echo "$USER ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USER \
    && chmod 0440 /etc/sudoers.d/$USER


COPY ../utilities/netauto_cron.cron /tmp/netauto_cron.cron
RUN chown netauto:netauto /tmp/netauto_cron.cron

USER netauto
RUN chmod 0644 /tmp/netauto_cron.cron  \
    && crontab /tmp/netauto_cron.cron

RUN pip3 install -r /tmp/requirements.txt

CMD ["/bin/bash", "cron -f &"]
 
