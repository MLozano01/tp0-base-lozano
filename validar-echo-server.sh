#!/bin/bash

docker run -it --network=tp0_testing_net --name=my_tester ubuntu sh

docker exec -it my_tester sh -c "apt update && apt install -y  netcat-traditional"

TEST_MESSAGE="Potter"

PORT="12345"

SERVER_ANS=$(docker exec -it my_tester sh -c "echo $TEST_MESSAGE | nc server $PORT | tr -d '\r'")

echo $SERVER_ANS

if [[ $SERVER_ANS = $TEST_MESSAGE ]]
then 
    echo "action: test_echo_server | result: success"
else 
    echo "action: test_echo_server | result: fail"
fi 