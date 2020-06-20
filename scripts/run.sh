#!/usr/bin/env bash

clear_interface () {
    tc qdisc delete dev enp0s8 root
}

trap "clear_interface; echo 'Reverting to original config'; exit" SIGHUP SIGINT SIGTERM

clear_interface

IFS=$'\n'
for line in `cat ../scenarios.txt`
do
    rectified=${line#$"echo 'CMurl@dmin213!' | sudo -S "}
    echo $rectified
    eval $rectified
    sleep 60
    clear_interface
done
