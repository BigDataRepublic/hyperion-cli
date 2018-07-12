FROM tensorflow/tensorflow:latest-gpu

RUN apt-get update && \
    apt-get install --no-upgrade -y apt-utils && \
    apt-get install --no-upgrade -y python3-pip && \
    pip3 install --upgrade pip && \
    /usr/local/bin/pip3 install tensorflow

COPY main.sh /opt/main.sh
COPY model.py /opt/model.py

WORKDIR /opt 

ENTRYPOINT ["/bin/bash"]
