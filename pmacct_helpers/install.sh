echo ' running installer'

git clone https://github.com/ntop/nDPI -b 4.8-stable
git clone https://github.com/pmacct/pmacct.git

echo 'dependencies'
sudo apt install autoconf automake
sudo apt install libtool
sudo apt install make
sudo apt install libpcap-dev
sudo apt install python3-pip


echo 'building nDPI'
cd nDPI
./autogen.sh
./configure
make
make install
ldconfig
cd ..

echo 'install mysql client'
sudo apt install mysql-client-core-8.0
sudo apt install libmysqlclient-dev
sudo apt install mysql-server

sudo apt install libnuma-dev 
sudo apt install g++

#sudo systemctl start mysqld  # may not be needed.
#sudo systemctl enable mysqld

echo 'building pmacct'
cd pmacct
./autogen
./configure --enable-ndpi --enable-mysql
make
make install
echo 'cleaning up'
cd ..
rm -rf pmacct
rm -rf nDPI

echo 'running sql scripts'
cd ..
sudo mysql -u root < sql/init.sql
sudo mysql -u root < sql/grant.sql

#python enviroment
#pip install PySide6
#pip install netifaces
#pip install mysql.connector