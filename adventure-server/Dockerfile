## Custom Dockerfile
#
# USE:
#    docker build . --no-cache -t johnnewcombe/telstar
#    docker login

#    docker push johnnewcombe/telstar
#    docker run --name telstar -d -p 6512:6512 -p johnnewcombe/telstar 6512
#
FROM ubuntu
LABEL maintainer="John Newcombe, https://glasstty.com"
ENV REFRESHED_AT 2020-11-29
ENV DEBIAN_FRONTEND="noninteractive" TZ="Europe/London"

RUN apt-get -y update \
        && apt-get -y install \
        git \
        nano \
        python3-tornado \
        python3-pip \
        && pip3 install adventure \
        && rm -rf /var/lib/apt/lists/*

# Add the startup script
COPY adventure_server.py advent80.dat advent40.dat /opt/adventureserver/

# copy the package
WORKDIR /opt/adventureserver

ENTRYPOINT ["python3", "-u", "adventure_server.py"]
