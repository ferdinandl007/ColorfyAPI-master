#!/bin/bash

sudo chmod 444 ssl_certificates/privkey.pem
docker build -f Dockerfile.dev --tag fl/colourize:nginx-dev .
sudo chmod 400 ssl_certificates/privkey.pem