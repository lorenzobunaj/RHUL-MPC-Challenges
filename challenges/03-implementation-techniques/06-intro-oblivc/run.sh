#!/bin/bash

./party2 &
sleep 1

socat TCP-LISTEN:1358,reuseaddr,fork EXEC:"./party1",pty,stderr