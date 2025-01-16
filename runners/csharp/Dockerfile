FROM baserunner
WORKDIR /app/
RUN apt-get update && \
    apt-get install -y wget apt-transport-https && \
    wget https://packages.microsoft.com/config/ubuntu/24.04/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y dotnet-sdk-8.0 aspnetcore-runtime-8.0
#RUN dotnet tool update -g linux-dev-certs && \
#    linux-dev-certs
COPY csharp-runner.sh .


RUN useradd -m runner

CMD ["python3", "/usr/src/app/runnerAPI.py"]