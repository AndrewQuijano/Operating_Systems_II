#!/bin/bash

sudo apt-get update
sudo apt-get install git

# Install basics
sudo apt-get install vim
sudo apt-get install dos2unix

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

# Update the packages, Written as of May 4, 2019
# You want sklearn 0.20.3 scipy 1.1.0 numpy 1.16.3
sudo pip3 install scipy -U
sudo pip3 install sklearn -U
sudo pip3 install numpy -U

# Install Java and Eclipse
sudo apt-get install default-jdk
sudo apt-get install default-jre
sudo add-apt-repository ppa:linuxuprising/java
sudo apt update
sudo apt-get install oracle-java11-installer


