FROM baserunner
RUN apt-get update && apt-get install -y ghc

WORKDIR /app/

COPY haskell-runner.sh .

CMD ["python3", "/usr/src/app/runnerAPI.py"]