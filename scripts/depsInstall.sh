#!/bin/bash

sudo apt install -y libzookeeper-mt-dev libboost-all-dev

wget https://github.com/protocolbuffers/protobuf/releases/download/v2.6.1/protobuf-2.6.1.tar.gz
tar -zxvf protobuf-2.6.1.tar.gz
cd protobuf-2.6.1

./configure
make
make check
sudo make install