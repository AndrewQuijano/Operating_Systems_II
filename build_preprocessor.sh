#!/bin/bash

mkdir build-files
cd build-files
cmake -DCMAKE_BUILD_TYPE=Debug -G "CodeBlocks - Unix Makefiles"
cd ..
cmake --build ./build-files --target kdd99extractor -- -j 4
build-files/src/kdd99extractor
