#!/usr/bin/env bash

stdbuf -oL iperf3 -c 192.168.2.22 -p 5201 -t 9999 -i 1 -f K > '../iperf_results/results.txt'
