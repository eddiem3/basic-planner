FROM kavrakilab/ompl


RUN apt-get update
RUN apt-get -y install libjpeg-dev zlib1g-dev libpng-dev
RUN pip3 install matplotlib
