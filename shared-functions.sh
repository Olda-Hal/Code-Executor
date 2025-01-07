#!/bin/bash
find_free_sandbox_id() {
    for id in $(seq 0 99); do
        if ! mkdir -p "/var/local/lib/isolate/$id/box" 2>/dev/null; then
            continue
        fi
        if ! flock -n "/var/local/lib/isolate/$id/box.lock" true 2>/dev/null; then
            rmdir "/var/local/lib/isolate/$id/box" 2>/dev/null
            continue
        fi
        echo $id
        return 0
    done
    echo "No free sandbox ID available" >&2
    return 1
}

cleanup_sandbox() {
    local id=$1
    isolate --cleanup --box-id=$id
    rm -f "/var/local/lib/isolate/$id/box.lock" 2>/dev/null
    rmdir "/var/local/lib/isolate/$id/box" 2>/dev/null
}
