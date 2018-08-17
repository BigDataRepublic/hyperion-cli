FROM tensorflow/tensorflow:latest-gpu-py3

COPY main.sh /opt/main.sh
COPY model.py /opt/model.py

WORKDIR /opt 

ENTRYPOINT ["/bin/bash"]
