#!/usr/bin/env bash

stdbuf -oL iperf3 -c 80.211.66.33 -p 5201 -t 9999 -i 1 -f K > '../iperf_results/results.txt'