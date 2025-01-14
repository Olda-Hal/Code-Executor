FROM baserunner
RUN apt-get update && apt-get install -y nasm

WORKDIR /app/

COPY asm-runner.sh .

CMD ["python3", "/usr/src/app/runnerAPI.py"]