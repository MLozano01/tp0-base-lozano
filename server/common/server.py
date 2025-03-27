import socket
import logging
import signal

import multiprocessing as mp

import common.server_protocol as protocol
import common.utils as utils

class Server:
    def __init__(self, port, listen_backlog, total_agency):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)
        self.total_agency = total_agency
        self.client_list = [None for i in range(total_agency)]
        self.agencies_talked_to = 0
        self.all_process = []


    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """

        signal.signal(signal.SIGTERM, self.hanlder)

        manager = mp.Manager()
        self.client_list = manager.list(self.client_list)

        lock = manager.Lock()

        queue = mp.Queue()

        process = mp.Process(target=self.handle_all_process, args=(queue,))
        process.start()

        self.all_process.append(process)
        
        while True:
            try:
                client_sock = self.__accept_new_connection()
                logging.info(f"action: run | result: success | message: new_connection")

                process = mp.Process(target=self.__handle_client_connection, args=(client_sock,lock,queue,)).start()

                self.all_process.append(process)

            except Exception as e:
                # logging.error(f"action: run | result: fail | error: {e}")
                break

    def __handle_client_connection(self, client_sock, lock, queue):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:            
            while True:
                data = self.rcvall(client_sock)
                action, all_good, info = protocol.parse_data(data, lock)
                
                if action == protocol.CLOSED:
                    logging.info("action: receive_message | result: success | message: CLOSED")
                    break

                if action == protocol.INFO:
                    logging.info(f"action: receive_message | result: success | message: INFO | info: {info}")
                    with lock:
                        self.client_list[info-1] = client_sock
                    client_sock.sendall("ACK\n".encode('utf-8'))
                    continue

                if action == protocol.DONE:
                    logging.info("action: receive_message | result: success | message: DONE")
                    queue.put(True)
                    break

                if not all_good:
                    client_sock.sendall("ERROR\n".encode('utf-8'))
                    return

                client_sock.sendall("ACK\n".encode('utf-8'))

        except OSError as e:
            logging.error(f"action: receive_message | result: fail | error: {e}")

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
        logging.info("action: exit | result: success")
        print("Server closed")

    def hanlder(self):
        self.close_server_socket()

    def rcvall(self, sock):
        expected_size = sock.recv(protocol.INT32_LEN)
        expected_size_int = int.from_bytes(expected_size, byteorder='big')
        data = bytearray()

        while len(data) < expected_size_int:
            part = sock.recv(1024)
            data.extend(part)

        final_data = bytearray()
        final_data.extend(expected_size)
        final_data.extend(data)
        return final_data
    
    def handle_contest(self):
        all_bets = utils.load_bets()
        winners = {}
        for bet in all_bets:
            if utils.has_won(bet):
                # logging.info("THERE IS A WINNER")
                winners[bet.agency] = winners.get(bet.agency, [])
                winners[bet.agency].append(bet)
        
        for agency in range(0, len(self.client_list)):
            # logging.info(f"action: winners_sent | result: in_progress")
            
            # logging.info(f"{winners.get(agency+1, [])}")

            msg = protocol.encode_winners(winners.get(agency+1, []))
            self.client_list[agency].sendall(msg.encode('utf-8'))
        
        logging.info("action: winners_sent | result: success")

    def handle_all_process(self, queue):
        processes_done = 0
        while processes_done < self.total_agency:
            logging.info(f"msg: {processes_done}")
            done = queue.get()
            if done:    
                processes_done += 1
        
        logging.info("action: sorteo | result: success")
        self.handle_contest()
        self.end()

    def end(self):
        for process in self.all_process:
            process.join()
            logging.info(f"action: closing thread | result: success | pid: {process.pid}")

        for client in self.client_list:
            client.close()
            logging.info(f"action: closing client | result: success")

        self.close_server_socket()