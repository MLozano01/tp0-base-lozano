import socket
import logging
import signal

from common.server_protocol import decode_bets
import common.utils as utils

class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """

        # TODO: Modify this program to handle signal to graceful shutdown
        # the server

        signal.signal(signal.SIGTERM, self.hanlder)

        while True:
            try:
                client_sock = self.__accept_new_connection()
                self.__handle_client_connection(client_sock)
            except Exception as e:
                logging.error(f"action: run | result: fail | error: {e}")
                break

    def __handle_client_connection(self, client_sock):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:            
            data = self.rcvall(client_sock)

            bets, all_good = decode_bets(data)


            if not all_good:
                logging.error(f"action: receive_message | result: fail | cantidad: {len(bets)}")
                client_sock.sendall("ERROR\n".encode('utf-8'))
                return

            utils.store_bets(bets)

            logging.info(f"action: apuesta_almacenada | result: success | cantidad: {len(bets)}")

            client_sock.sendall("ACK\n".encode('utf-8'))

        except OSError as e:
            logging.error("action: receive_message | result: fail | error: {e}")


    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        logging.info('action: accept_connections | result: in_progress')
        c, addr = self._server_socket.accept()
        logging.info(f'action: accept_connections | result: success | ip: {addr[0]}')
        return c

    def close_server_socket(self):
        """
        Close server socket

        Function that closes the server socket
        """
        self._server_socket.shutdown(socket.SHUT_RDWR)
        self._server_socket.close()
        logging.info("action: close_server_socket | result: success")
        print("Server closed")

    def hanlder(self, signum, frame):
        self.close_server_socket()

    def rcvall(self, sock):
        expected_size = sock.recv(4)
        expected_size_int = int.from_bytes(expected_size, byteorder='big')
        data = bytearray()

        while len(data) < expected_size_int:
            part = sock.recv(32)
            data.extend(part)

        final_data = bytearray()
        final_data.extend(expected_size)
        final_data.extend(data)
        return final_data