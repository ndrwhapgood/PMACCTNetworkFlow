#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
##############################################################################
# 1) Start fresh
##############################################################################
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi
sudo rm -rf /usr/local/include/ndpi
sudo rm -f  /usr/local/lib/libndpi.so*
sudo rm -f  /usr/local/lib/pkgconfig/libndpi*.pc
sudo ldconfig
cd
sudo rm -r src/
##############################################################################
# 2) Build and install nDPI 4.6
##############################################################################
mkdir src
cd src/
rm -rf nDPI
git clone  --branch 4.6 https://github.com/ntop/nDPI.git
cd nDPI
./autogen.sh
./configure --prefix=/usr/local
make -j"$(nproc)"
sudo make install
sudo ldconfig
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
pkg-config --modversion libndpi         # 4.6
pkg-config --cflags libndpi             # -I/usr/local/include/ndpi
ARCH=$(dpkg-architecture -qDEB_HOST_MULTIARCH)
sudo ln -sf /usr/local/lib/pkgconfig/libndpi.pc /usr/lib/$ARCH/pkgconfig/libndpi.pc
sudo ln -sf /usr/local/lib/pkgconfig/libndpi.pc /usr/lib/$ARCH/pkgconfig/ndpi.pc
##############################################################################
# 3) Build and Install PMACCT 1.7.9
##############################################################################
cd ~/src
git clone --depth 1 --branch 1.7.9 \
          https://github.com/pmacct/pmacct.git
cd pmacct
git submodule update --init --recursive       # pulls libcdada and other deps
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
make distclean || true
./autogen.sh
./configure --enable-ndpi NDPI_CFLAGS="-I/usr/local/include/ndpi" NDPI_LIBS="-L/usr/local/lib -lndpi"
make -j"$(nproc)"
sudo make install
##############################################################################
# 4) Verify
##############################################################################
pmacctd -V
