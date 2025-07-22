#!/bin/bash

socat TCP-LISTEN:1358,reuseaddr,fork EXEC:"./main 1",pty,stderr