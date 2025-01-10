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
    zsh \
    sudo

apt install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa -y

apt-get -y update && apt-get install -y \
    python3.13 \
    python3.14 \
    python3.12-venv \
    python3.13-venv \
    python3.14-venv \
    python3.12-dev \
    python3.13-dev \
    python3.14-dev \
    python3-pip

# 安装 UPX (Ultimate Packer for eXecutables)。
cd /tmp \
    && wget https://github.com/upx/upx/releases/download/v4.2.4/upx-4.2.4-amd64_linux.tar.xz \
    && tar -xf upx-4.2.4-amd64_linux.tar.xz \
    && cp upx-4.2.4-amd64_linux/upx /usr/local/bin/ \
    && chmod +x /usr/local/bin/upx \
    && rm -rf upx-4.2.4-amd64_linux* \
    && upx --version