FROM python:slim-bookworm

WORKDIR /workspaces


ARG USER=netauto
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update \
    && apt install -y --no-install-recommends sudo \
    && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install pipenv \
    && useradd -ms /bin/bash $USER \
    && echo "$USER ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USER \
    && chmod 0440 /etc/sudoers.d/$USER


COPY ./requirements.txt /tmp/requirements.txt

RUN pipenv install --skip-lock --requirements /tmp/requirements.txt \
    && rm -f /tmp/requirements.txt



CMD ["/bin/bash"]
 
