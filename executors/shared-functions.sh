#!/bin/bash

find_free_sandbox_id() {
    local attempts=0
    while [ $attempts -lt 10 ]; do
        id=$((RANDOM % 1000000 + 1))
        echo "Generated ID: $id" >&2
        if [ ! -d "/var/local/lib/isolate/$id/box" ]; then
            echo $id
            return 0
        fi
        echo "Directory /var/local/lib/isolate/$id/box already exists" >&2
        attempts=$((attempts + 1))
    done
    echo "Failed to find a free sandbox ID" >&2
    return 1
}

cleanup_sandbox() {
    local id=$1
    isolate --cleanup --box-id=$id
    rm -f "/var/local/lib/isolate/$id/box.lock" 2>/dev/null
    rmdir "/var/local/lib/isolate/$id/box" 2>/dev/null
}