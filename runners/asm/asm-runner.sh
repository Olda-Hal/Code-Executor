#!/bin/bash

mkdir -p /run/user/$(id -u)
echo "$CODE" > /run/user/$(id -u)/script.s
chmod 777 /run/user/$(id -u)/script.s


output=$(exec bwrap --ro-bind /usr /usr \
    --dir /tmp \
    --dir /var \
    --symlink ../tmp var/tmp \
    --proc /proc \
    --dev /dev \
    --ro-bind /etc/resolv.conf /etc/resolv.conf \
    --symlink usr/lib /lib \
    --symlink usr/lib64 /lib64 \
    --symlink usr/bin /bin \
    --symlink usr/sbin /sbin \
    --bind /run/user/$(id -u) /run/user/$(id -u) \
    --chdir / \
    --unshare-all \
    --die-with-parent \
    --dir /run/user/$(id -u) \
    --setenv XDG_RUNTIME_DIR "/run/user/$(id -u)" \
    --setenv PS1 "bwrap-demo$ " \
    /bin/bash -c "nasm -f elf64 /run/user/$(id -u)/script.s -o /run/user/$(id -u)/script.o && ld /run/user/$(id -u)/script.o -o /run/user/$(id -u)/program && /run/user/$(id -u)/program")
echo "$output"
