#!/bin/bash

docker build --target builder --tag fl/colourize:builder .
docker build --target pip_install --tag fl/colourize:pip_install .
docker build --target prepare_release --tag fl/colourize:prepare_release .
docker build --target release --tag fl/colourize:release .