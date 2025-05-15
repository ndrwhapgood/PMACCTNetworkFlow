echo ' running installer'

git clone https://github.com/ntop/nDPI -b 4.8-stable
git clone https://github.com/pmacct/pmacct.git

echo 'nDPI dependencies'
sudo apt install autoconf automake
sudo apt install libtool
sudo apt install make
sudo apt install libpcap-dev # libpcap-devel in rhel

echo 'building nDPI'
cd nDPI
./autogen.sh
./configure
make
make install
ldconfig
cd ..

echo 'install mysql client'
sudo apt install mysql-client-core-8.0 # dnf install mysql-server
sudo apt install libmysqlclient-dev
sudo apt install mysql-server

sudo apt install libnuma-dev 

sudo apt install g++

#sudo systemctl start mysqld
#sudo systemctl enable mysqld

echo 'building pmacct'
cd pmacct
./autogen
./configure --enable-ndpi --enable-mysql
make #issue here: error: pathspec 'src/external_libs/libcdada' did not match any file(s) known to git
#potential source of the problem is file name conflicts with the make, works fine when I change dirs and install there.
make install
#solution was to change directories, since our back dir has the same name

echo 'cleaning up'
cd ..
rm pmacct-1.7.9.tar.gz
rm -rf pmacct-1.7.9
rm -rf nDPI

echo 'running sql scripts'
sudo mysql -u root -p < sql/init.sql
sudo mysql -u root -p < sql/grant.sql