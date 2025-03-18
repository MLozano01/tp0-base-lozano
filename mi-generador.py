import sys

def docker_yaml_generator(file_name, client_amount):

    with open(file_name, 'w') as f:
        f.write(create_yaml_file(client_amount))

def create_yaml_file(client_amount):
    clients = join_clients(client_amount)
    server = create_server()
    network = create_network()
    content = f"""
name: tp0
services:
  {server}
  {clients}
networks:
  {network}
"""
    return content

def join_clients(amount):
    clients = ""
    for client in range(1, amount+1):
        clients += create_client(client)
    return clients

def create_client(id):
    client = f"""
  client{id}:
    container_name: client{id}
    image: client:latest
    entrypoint: /client
    environment:
      - CLI_ID={id}
    networks:
      - testing_net
    depends_on:
      - server\n
    volumes:
      - ./client/config.yaml:/config.yaml
    """ 
    return client

def create_server():
    server = f"""server:
    container_name: server
    image: server:latest
    entrypoint: python3 main.py
    environment:
      - PYTHONUNBUFFERED=1
      - LOGGING_LEVEL=DEBUG
    networks:
      - testing_net
    volumes:
      - ./server/config.ini:/config.ini
    """
    return server

def create_network():
    network = f"""testing_net:
    ipam:
      driver: default
      config:
        - subnet: 172.25.125.0/24
    """
    return network

def main(file_name, client_amount):
    docker_yaml_generator(file_name, client_amount)

if __name__ == "__main__":
    main(file_name=sys.argv[1], client_amount=int(sys.argv[2]))