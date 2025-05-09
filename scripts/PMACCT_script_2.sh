#!/usr/bin/sh
sudo apt-get update
sudo apt-get install -y \
  build-essential \
  git \
  autoconf \
  automake \
  libtool \
  pkg-config \
  libpcap-dev \
  libjson-c-dev \
  libmaxminddb-dev \
  librrd-dev \
  libnuma-dev \
  libpcre2-dev

git clone https://github.com/pmacct/pmacct.git

cd pmacct

./autogen.sh

./configure --with-ndpi

make

sudo make install

sudo ldconfig
