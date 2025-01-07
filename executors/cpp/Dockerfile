FROM gcc:latest

WORKDIR /app
COPY runner.sh /app/
RUN chmod +x /app/runner.sh

ENV CODE=""
ENV INPUT=""

CMD ["/app/runner.sh"]