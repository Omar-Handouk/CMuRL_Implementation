#!/usr/bin/env bash

clear_interface () {
    tc qdisc delete dev enp0s8 root
}

trap "clear_interface; echo 'Reverting to original config'; exit" SIGHUP SIGINT SIGTERM

clear_interface

i=1
IFS=$'\n'
for line in `cat ../scenarios.txt`
do
    rest=$((i%3))
    if [ $rest -eq 0 ]; then
        echo '>>Rest state<<'
    else
        rectified=${line#$"echo 'CMurl@dmin213!' | sudo -S "}
        echo $rectified
        eval $rectified
    fi
    sleep 20
    clear_interface
    i=$((i+1))
done
