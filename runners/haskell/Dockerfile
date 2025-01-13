FROM baserunner

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libffi-dev \
    libffi8ubuntu1 \
    libgmp-dev \
    libgmp10 \
    libncurses-dev

RUN curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh

RUN echo ". /root/.ghcup/env" >> /etc/profile \
    && echo ". /root/.ghcup/env" >> /root/.bashrc

WORKDIR /app/

COPY haskell-runner.sh .

CMD ["python3", "/usr/src/app/runnerAPI.py"]
