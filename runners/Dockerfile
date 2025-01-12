FROM ubuntu:latest as runnerbase

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Vytvoření a aktivace virtuálního prostředí
RUN python3 -m venv /usr/src/app/venv
ENV PATH="/usr/src/app/venv/bin:$PATH"

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY runnerAPI.py /usr/src/app/

CMD ["python3", "/usr/src/app/runnerAPI.py"]