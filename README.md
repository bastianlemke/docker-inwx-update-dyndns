# docker-inwx-update-dyndns

Docker image for that updates a DynDNS account on inwx.com

Based on this python script:
https://github.com/nroi/inwx_update_dyndns

## Running container

````bash
docker run -d \
	-e IPV6_ENABLED=true \
	-e USERNAME=<username> \
	-e PASSWORD=<password> \
````