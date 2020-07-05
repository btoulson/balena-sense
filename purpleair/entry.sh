#!/bin/bash

# We compare the version of the BSEC library download here
# If it has changed we remove the existing config and state data as they aren't compatible between versions

mkdir -p /data/purpleair
cp /usr/src/app/version /data/purpleair/version

echo "================ Starting Balena PurpleAir ================"

exec python /usr/src/app/scripts/purpleair.py
