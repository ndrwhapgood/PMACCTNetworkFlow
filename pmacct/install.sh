echo ' running installer'

get clone clone https://github.com/ntop/nDPI -b 4.4-stable
wget --no-check-certificate --content-disposition http://www.pmacct.net/pmacct-1.7.8.tar.gz
tar zxvf pmacct-1.7.8.tar.gz

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

echo 'building pmacct'
cd pmacct-1.7.8
./configure --enable-ndpi --enable-mysql
make
make install

echo 'cleaning up'
cd ..
rm pmacct-1.7.8.tar.gz
rm -rf pmacct-1.7.8
rm -rf nDPI

echo 'running sql scripts'
sudo mysql -u root -p < sql/init.sql
sudo mysql -u root -p < sql/grant.sql