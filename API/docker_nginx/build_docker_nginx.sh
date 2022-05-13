#!/bin/bash

sudo chmod 444 ssl_certificates/privkey.pem
sudo chmod 444 password/.htpasswd

docker build --tag fl/colourize:nginx .

sudo chmod 400 ssl_certificates/privkey.pem
sudo chmod 600 password/.htpasswd

