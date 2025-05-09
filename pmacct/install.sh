echo ""
#echo "We will now install sofware for generating data from network interfaces (pmacct)"
#echo "This will take some time to complete, press enter to continue:"
#read resp

#
# Install pmacct for collecting network flow data
#
if ! [ -x "$(command -v pmacctd)" ]; then
# Obtain 1.7.7 version of pmacct and make/install
wget --no-check-certificate --content-disposition http://www.pmacct.net/pmacct-1.7.7.tar.gz
tar zxvf pmacct-1.7.7.tar.gz

echo ""
echo "Building pmacct..."
echo ""
cd pmacct-1.7.7
./configure
make
echo "Installing pmacct..."
echo ""
make install
cd ..
rm pmacct-1.7.7.tar.gz
rm -rf pmacct-1.7.7
else
echo "pmacct already installed."
fi