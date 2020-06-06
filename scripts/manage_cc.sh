#!/usr/bin/env bash

write() {
    printf "%s" "$2" > "/sys/module/tcp_tuner/parameters/$1"
}

die() {
    echo "$*" >&2
    exit 1
}

main() {
    [[ -z $2 ]] && die "You need to pass a property to modify as a first parameter and a value as the second"

    case $1 in
        alpha|beta)
            write "$1" "$2"
            ;;
        tcp_friendliness|fast_convergence)
            if [[ "$2" == "0" || "$2" == "1" ]]; then
                write "$1" "$2"
            else
                die "This parameter only accepts a boolean value (0/1)"
            fi
            ;;
        *)  die "The only accepted values for first parameter are alpha/beta/tcp_friendliness/fast_convergence"
            ;;
    esac
}

main "$@"