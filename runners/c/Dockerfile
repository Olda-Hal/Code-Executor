FROM baserunner
RUN apt-get update && apt-get install -y gcc

WORKDIR /app/

COPY c-runner.sh .

CMD ["python3", "/usr/src/app/runnerAPI.py"]