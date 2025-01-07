FROM base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy isolate configuration
COPY isolate.conf /etc/isolate.conf

# Copy shared functions script and set permissions
COPY shared-functions.sh /shared-functions.sh
RUN chmod +x /shared-functions.sh

# Create directory for isolate boxes and set ownership
RUN mkdir -p /var/local/lib/isolate 
RUN chown -R executor:executor /var/local/lib/isolate

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]