#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo >>/dev/stderr "usage: autologin.sh <login-host> <login-password> <secret-key>"
    # exit -1
fi

HOST="180.76.169.250"
PASSWD=="Paddle@987654"
USER="root"

# seckey="#"
# verification_code=`python -c "import googauth; print googauth.generate_code('$seckey')"`

expect -c ' \
    set HOST "'$HOST'"
    set PASSWD "'$PASSWD'"
    # set verification_code "'$verification_code'"
    set USER "'$USER'"

    spawn ssh -X $USER@$HOST
    # expect "*Verification code*" {
    #    send "$verification_code\r"
    # }
    expect "*Password*" {
        send "$PASSWD\r"
    }
    expect "*Enter*" {
        send "1\r"
    }
    # expect "*input server IP*" {
    #     send "$HOST\r"
    # }
    expect "*password*" {
        send "$PASSWD\r"
        send "tmux a -t root\r"
    }
    interact
'
