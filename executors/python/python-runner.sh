#!/bin/bash

source /shared-functions.sh

# get free sandbox ID
SANDBOX_ID=$(find_free_sandbox_id)
if [ $? -ne 0 ]; then
    echo "Failed to allocate sandbox"
    exit 1
fi

# isolate init
isolate --init --box-id=$SANDBOX_ID

# Create files
echo "$CODE" > /var/local/lib/isolate/$SANDBOX_ID/box/code.py
echo "$INPUT" > /var/local/lib/isolate/$SANDBOX_ID/box/input.txt
touch /var/local/lib/isolate/$SANDBOX_ID/meta.txt
# run code
isolate --box-id=$SANDBOX_ID \
    --time=5 \
    --wall-time=10 \
    --mem=512000 \
    --processes=32 \
    --stdin=input.txt \
    --meta=/var/local/lib/isolate/$SANDBOX_ID/meta.txt \
    --run -- python3 code.py

RESULT=$?

# read meta info
if [ -f "/var/local/lib/isolate/$SANDBOX_ID/meta.txt" ]; then
    cat "/var/local/lib/isolate/$SANDBOX_ID/meta.txt"
fi

# Cleanup
cleanup_sandbox $SANDBOX_ID
exec 9>&-

exit $RESULT