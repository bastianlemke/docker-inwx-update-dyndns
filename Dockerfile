FROM alpine:latest

MAINTAINER Bastian Lemke

RUN apk add gettext curl python3 py3-toml py3-requests

COPY data/inwx_update_dyndns.toml.template /inwx_update_dyndns.toml.template
COPY data/inwx_update_dyndns.py /inwx_update_dyndns.py

COPY data/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]