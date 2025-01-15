#!/bin/bash

mkdir -p /run/user/$(id -u)
echo "$PROJECT" | xxd -r -p > /run/user/$(id -u)/script.tar.gz
mkdir -p /run/user/$(id -u)/project
gunzip /run/user/$(id -u)/script.tar.gz
tar --warning=no-unknown-keyword -xf /run/user/$(id -u)/script.tar -C /run/user/$(id -u)/project/
chmod -R 777 /run/user/$(id -u)/project/
output=$(exec timeout $TIMEOUT bwrap --ro-bind /usr /usr \
    --dir /tmp \
    --dir /var \
    --symlink ../tmp var/tmp \
    --proc /proc \
    --dev /dev \
    --ro-bind /etc/resolv.conf /etc/resolv.conf \
    --symlink usr/lib /lib \
    --symlink usr/lib64 /lib64 \
    --symlink usr/bin /bin \
    --symlink /root/.ghcup /ghcup \
    --symlink usr/sbin /sbin \
    --bind /run/user/$(id -u) /run/user/$(id -u) \
    --chdir / \
    --unshare-all \
    --die-with-parent \
    --dir /run/user/$(id -u) \
    --setenv XDG_RUNTIME_DIR "/run/user/$(id -u)" \
    --setenv PS1 "bwrap-demo$ " \
    /bin/bash -c "/ghcup/ghc/9.4.8/bin/ghc-9.4.8 -o /run/user/$(id -u)/project/program /run/user/$(id -u)/project/$EXECFILE && /run/user/$(id -u)/project/program")
echo "$output"

rm -rf /run/user/$(id -u)/
#     #/bin/bash -c "ls /ghcup -la")
