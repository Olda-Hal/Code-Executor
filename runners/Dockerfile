FROM ubuntu:latest as baserunner

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv xxd

# creation of venv
RUN python3 -m venv /usr/src/app/venv
ENV PATH="/usr/src/app/venv/bin:$PATH"

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# api interface
COPY runnerAPI.py /usr/src/app/

# Install bubblewrap
RUN apt-get update && apt-get install -y bubblewrap

# Set up bubblewrap
RUN ln -s /usr/bin/bwrap /usr/local/bin/bwrap