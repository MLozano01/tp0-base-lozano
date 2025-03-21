#!/bin/bash

docker run --network=tp0_testing_net --name=server_tester ubuntu sh

docker exec server_tester sh -c "apt update && apt install -y  netcat-openbsd"

TEST_MESSAGE="Malfoy"

PORT="12345"

SERVER_ANS=$(docker exec server_tester sh -c "echo $TEST_MESSAGE | nc server $PORT | tr -d '\r\n'")

# echo $SERVER_ANS

# n=$(expr length "$SERVER_ANS")
# echo "Length of the string is : $n"


if [ "$SERVER_ANS" = "$TEST_MESSAGE" ]
then 
    echo "action: test_echo_server | result: success"
else 
    echo "action: test_echo_server | result: fail"
fi

docker stop server_tester
docker rm server_tester