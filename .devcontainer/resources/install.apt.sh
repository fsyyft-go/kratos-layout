#!/bin/bash
set -e

# 安装基础工具、网络工具和开发工具。
apt-get -y update && apt-get install -y \
    locales \
    coreutils \
    util-linux \
    procps \
    psmisc \
    lsof \
    strace \
    file \
    which \
    locate \
    jq \
    telnet \
    iputils-ping \
    iproute2 \
    curl \
    wget \
    net-tools \
    dnsutils \
    traceroute \
    netcat-openbsd \
    tcpdump \
    nmap \
    iftop \
    mtr \
    socat \
    gdb \
    sysstat \
    vim \
    nano \
    emacs-nox \
    git \
    tree \
    htop \
    less \
    grep \
    sed \
    gawk \
    unzip \
    zip \
    tar \
    rsync \
    tmux \
    screen \
    build-essential \
    make \
    openssh-server \
    zsh

# 安装 UPX (Ultimate Packer for eXecutables)。
cd /tmp \
    && wget https://github.com/upx/upx/releases/download/v4.2.4/upx-4.2.4-amd64_linux.tar.xz \
    && tar -xf upx-4.2.4-amd64_linux.tar.xz \
    && cp upx-4.2.4-amd64_linux/upx /usr/local/bin/ \
    && chmod +x /usr/local/bin/upx \
    && rm -rf upx-4.2.4-amd64_linux* \
    && upx --version