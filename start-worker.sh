#!/bin/sh
# Start a worker instance: rebuild the worker image and run it.
set -ex
./build-master.sh
./run-master.sh $@