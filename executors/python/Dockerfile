FROM base as python-executor

# Copy the script and set permissions
COPY ./python-runner.sh /python-runner.sh
RUN chmod +x /python-runner.sh

# Debug: Print the script content and permissions
RUN ls -l /python-runner.sh && cat /python-runner.sh

# Ensure the script has the correct shebang
RUN head -n 1 /python-runner.sh | grep -q '^#!/'

# Set the entrypoint to the script
CMD ["/python-runner.sh"]