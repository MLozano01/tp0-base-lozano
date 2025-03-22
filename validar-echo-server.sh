#!/bin/bash

TEST_MESSAGE="Malfoy"

PORT="12345"

NET="tp0_testing_net"

C_NAME="server_tester"

SERVER_ANS=$(docker run --network=$NET --name=$C_NAME busybox sh -c "echo $TEST_MESSAGE | nc -w 5 server $PORT")

# docker exec server_tester sh -c "apt update && apt install -y  netcat-openbsd"

# SERVER_ANS=$(docker exec server_tester sh -c "echo $TEST_MESSAGE | nc -w 5 server $PORT | tr -d '\r\n'")

# echo $SERVER_ANS

# n=$(expr length "$SERVER_ANS")
# echo "Length of the string is : $n"

if [ "$SERVER_ANS" = "$TEST_MESSAGE" ]
then 
    echo "action: test_echo_server | result: success"
else 
    echo "action: test_echo_server | result: fail"
fi 