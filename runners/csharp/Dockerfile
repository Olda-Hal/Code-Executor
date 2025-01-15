FROM baserunner
WORKDIR /app/
RUN apt-get update && \
    apt-get install -y wget apt-transport-https && \
    wget https://packages.microsoft.com/config/ubuntu/24.04/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y dotnet-sdk-8.0 && \
    rm packages-microsoft-prod.deb
COPY csharp-runner.sh .
CMD ["python3", "/usr/src/app/runnerAPI.py"]