#!/bin/sh

envsubst < /inwx_update_dyndns.toml.template > /etc/inwx_update_dyndns.toml

python3 /inwx_update_dyndns.py