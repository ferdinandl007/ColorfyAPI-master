#!/bin/bash
docker build -f Dockerfile.gpu --target base --tag fl/colourize:base .
docker build -f Dockerfile.gpu --target builder --tag fl/colourize:builder .
docker build -f Dockerfile.gpu --target pip_install --tag fl/colourize:pip_install .
docker build -f Dockerfile.gpu --target prepare_release --tag fl/colourize:prepare_release .
docker build -f Dockerfile.gpu --target release --tag fl/colourize:release .