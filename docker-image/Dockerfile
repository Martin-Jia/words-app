FROM ubuntu:18.04
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-distutils \
        curl \
        ssh
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py
COPY requirements.txt /
RUN pip3 install -r /requirements.txt
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8