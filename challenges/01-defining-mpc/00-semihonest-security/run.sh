#!/bin/sh

# start the Python server in the background
python3 ./files/server.py

# forward 0.0.0.0:1337 to 127.0.0.1:1337
# exec socat TCP-LISTEN:1337,reuseaddr,fork TCP:127.0.0.1:1337