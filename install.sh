#!/bin/bash

# Install Python and packages
sudo apt-get install python3-pip
sudo apt-get install tcpdump python3-crypto ipython3
sudo apt-get install python3-tk

# Install Python and packages used by IDS and Fuzzer
sudo pip3 install --pre scapy[complete]
sudo pip3 install sklearn
sudo pip3 install matplotlib
sudo pip3 install pandas
sudo pip3 install pyshark
sudo pip3 install joblib
sudo pip3 install pikepdf
sudo pip3 install scikit-plot

# More Attack packages
sudo pip3 install pexpect
sudo pip3 install python-nmap

# Dependancies for Bro/Zeek
# Works for C+++ preprocessor
sudo apt-get install cmake make gcc g++ flex bison 
sudo apt-get install libpcap-dev libssl-dev python-dev swig zlib1g-dev

# Install Bro/Zeek from source
sudo apt-get install git
git clone --recursive https://github.com/zeek/zeek
cd ./zeek
./configure
make
sudo make install
sudo make install-aux
export PATH=/usr/local/zeek/bin:$PATH
cd ..
rm -rf ./zeek
