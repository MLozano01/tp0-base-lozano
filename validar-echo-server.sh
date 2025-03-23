#!/bin/bash

TEST_MESSAGE="Malfoy"

PORT="12345"

NET="tp0_testing_net"

C_NAME="server_tester"

SERVER_ANS=$(docker run --rm --network=$NET --name=$C_NAME busybox sh -c "echo $TEST_MESSAGE | nc -w 5 server $PORT")

if [ "$SERVER_ANS" = "$TEST_MESSAGE" ]
then 
    echo "action: test_echo_server | result: success"
else 
    echo "action: test_echo_server | result: fail"
fi