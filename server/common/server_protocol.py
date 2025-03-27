import logging

import common.utils as utils

NAME_CODE = 1
SURNAME_CODE = 2
ID_CODE = 3
BIRTHDATE_CODE = 4
NUMBER_CODE = 5
END_BET = 6

BET = 1
CLOSED = 2
INFO = 3
DONE = 4

INT32_LEN = 4
INT16_LEN = 2
INT8_LEN = 1

# Protocol 
# 0. Total length (int32)
# 1. NAME_CODE (int32) | length (int32) | name (string)
# 2. SURNAME_CODE (int32) | length (int32) | surname (string)
# 3. ID_CODE (int32) | id (int32)
# 4. BIRTHDATE_CODE (int32) | length (int32) | birthdate (string)
# 5. NUMBER_CODE (int32) | number (int32)

def parse_data(data):
    total_bytes_rcv = 0
    total_bytes_rcv += INT32_LEN

    action = int.from_bytes(data[total_bytes_rcv:total_bytes_rcv+INT8_LEN], byteorder='big')
    total_bytes_rcv += INT8_LEN

    if action == BET:
        logging.info(f"action: parse_data | result: success | message: BET")
        all_good = decode_bets(data[total_bytes_rcv:])
        return action, all_good, 0
    
    elif action == CLOSED:
        logging.info(f"action: parse_data | result: success | message: CLOSED")
        return action, True, 0

    elif action == INFO:
        logging.info(f"action: parse_data | result: success | message: INFO")
        info = decode_info(data[total_bytes_rcv:])
        return action, True, info
    
    elif action == DONE:
        logging.info(f"action: parse_data | result: success | message: DONE")
        return action, True, 0

    logging.error(f"action: parse_data | result: fail | error: action")

def decode_bets(bet_info):
    total_bytes_rcv = 0
    bets = []
    all_good = True

    agency = int.from_bytes(bet_info[total_bytes_rcv:total_bytes_rcv+INT8_LEN], byteorder='big')
    total_bytes_rcv += INT8_LEN

    while total_bytes_rcv != len(bet_info):

        code = int.from_bytes(bet_info[total_bytes_rcv:total_bytes_rcv+INT8_LEN], byteorder='big')
        total_bytes_rcv += INT8_LEN

        if code == NAME_CODE:
            name, total_bytes_rcv = decode_str(bet_info, total_bytes_rcv)

        elif code == SURNAME_CODE:
            surname, total_bytes_rcv = decode_str(bet_info, total_bytes_rcv)

        elif code == ID_CODE:
            document, total_bytes_rcv = decode_str(bet_info, total_bytes_rcv)

        elif code == BIRTHDATE_CODE:
            birthdate, total_bytes_rcv = decode_str(bet_info, total_bytes_rcv)

        elif code == NUMBER_CODE:
            number, total_bytes_rcv = decode_str(bet_info, total_bytes_rcv)
        
        elif code == END_BET:
            bet = utils.Bet(agency, name, surname, document, birthdate, number)
            all_good = check_bet(bet)
            if not all_good:
                logging.error(f"action: receive_message | result: fail | cantidad: {len(bets)}")
                return all_good
            bets.append(bet)

    utils.store_bets(bets)
    logging.info(f"action: apuesta_recibida | result: success | cantidad: {len(bets)}")

    return all_good


def decode_str(bet_info, total_bytes_rcv):
    str_len = int.from_bytes(bet_info[total_bytes_rcv:total_bytes_rcv+INT16_LEN], byteorder='big')
    total_bytes_rcv += INT16_LEN
    decoded_str = bet_info[total_bytes_rcv:total_bytes_rcv+str_len].decode('utf-8')
    total_bytes_rcv += str_len
    return decoded_str, total_bytes_rcv

def check_bet(bet):
    all_good = True

    if bet.agency <= 0:
        logging.error(f"action: check_bet | result: fail | error: agency")
        all_good = False
    if not bet.first_name:
        logging.error(f"action: check_bet | result: fail | error: name")
        all_good = False
    if not bet.last_name:
        logging.error(f"action: check_bet | result: fail | error: surname")
        all_good = False
    if not bet.document:
        logging.error(f"action: check_bet | result: fail | error: document")
        all_good = False
    if not bet.birthdate:
        logging.error(f"action: check_bet | result: fail | error: birthdate")
        all_good = False
    if bet.number < 0:
        logging.error(f"action: check_bet | result: fail | error: number")
        all_good = False
    return all_good

def decode_info(data):
    total_bytes_rcv = 0

    info = int.from_bytes(data[total_bytes_rcv:total_bytes_rcv+INT8_LEN], byteorder='big')
    return info

def encode_winners(winners):
    
    if len(winners) == 0:
        return "NO_WINNERS\n"

    winners_msg = "WINNERS\n"

    for winner in winners:
        winners_msg += f"{winner},"

    winners_msg = winners_msg[:-1]

    winners_msg += "\n"

    logging.info(f"action: encode_winners | result: success | winners: {winners_msg}")

    return winners_msg

