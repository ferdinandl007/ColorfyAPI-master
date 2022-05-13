FROM mcr.microsoft.com/azure-functions/python:2.0 as base

FROM base as builder
RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN apt-get update && apt-get install -y gcc build-essential wget

RUN pip install --user Bottleneck==1.3.2

FROM builder as pip_install

RUN pip install --user -r /requirements.txt

FROM base as download_weights

RUN mkdir /install

RUN mkdir /install/models
RUN mkdir /install/test_images
RUN mkdir /install/results_images

RUN wget https://www.dropbox.com/s/zkehq1uwahhbc2o/ColorizeArtistic_gen.pth?dl=0 -O /install/models/ColorizeArtistic_gen.pth
RUN wget https://download.pytorch.org/models/resnet34-333f7ec4.pth -O /install/models/resnet34-333f7ec4.pth


# RUN pip install --install-option="--prefix=/install" Bottleneck==1.3.2

# RUN pip install --install-option="--prefix=/install" -r /requirements.txt

# COPY --from=builder /install /usr/local

FROM base as release

COPY --from=pip_install /home/.local /home/.local
COPY . /home/site/wwwroot
COPY --from=download_weights /install /home/site/wwwroot

ENV PATH=/root/.local/bin:$PATH
ENV AzureWebJobsScriptRoot=/home/site/wwwroot
ENV AzureFunctionsJobHost__Logging__Console__IsEnabled=true

RUN cd /home/site/wwwroot 

RUN echo "Deployed site files are:"
RUN echo $PWD