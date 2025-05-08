#!/usr/bin/sh

sudo apt-get update

sudo apt-get install -y \
  build-essential \
  git \
  gettext \
  flex \
  bison \
  libtool \
  autoconf \
  automake \
  pkg-config \
  libpcap-dev \
  libjson-c-dev \
  libnuma-dev \
  libpcre2-dev \
  libmaxminddb-dev \
  librrd-dev

git clone https://github.com/ntop/nDPI.git
cd nDPI
./autogen.sh
make
sudo make install
sudo ldconfig
