
NAME_CODE = 1
SURNAME_CODE = 2
ID_CODE = 3
BIRTHDATE_CODE = 4
NUMBER_CODE = 5

INT32_LEN = 4

# Protocol 
# 0. Total length (int32)
# 1. NAME_CODE (int32) | length (int32) | name (string)
# 2. SURNAME_CODE (int32) | length (int32) | surname (string)
# 3. ID_CODE (int32) | id (int32)
# 4. BIRTHDATE_CODE (int32) | length (int32) | birthdate (string)
# 5. NUMBER_CODE (int32) | number (int32)

def decode_bet(bet_info):
    total_bytes_rcv = 0

    total_bytes_sent = bet_info[:INT32_LEN]
    total_bytes_rcv += INT32_LEN

    while total_bytes_rcv != len(bet_info):

        code = int.from_bytes(bet_info[total_bytes_rcv:INT32_LEN], byteorder='big')
        total_bytes_rcv += INT32_LEN

        if code == NAME_CODE:
            name_len = int.from_bytes(bet_info[total_bytes_rcv:INT32_LEN], byteorder='big')
            total_bytes_rcv += INT32_LEN
            name = bet_info[total_bytes_rcv:name_len].decode('utf-8')
            total_bytes_rcv += name_len

        elif code == SURNAME_CODE:
            surname_len = int.from_bytes(bet_info[total_bytes_rcv:INT32_LEN], byteorder='big') 
            total_bytes_rcv += INT32_LEN
            surname = bet_info[total_bytes_rcv:surname_len].decode('utf-8')
            total_bytes_rcv += surname_len

        elif code == ID_CODE:
            document_len = int.from_bytes(bet_info[total_bytes_rcv:INT32_LEN], byteorder='big') 
            total_bytes_rcv += INT32_LEN
            document = bet_info[total_bytes_rcv:document_len].decode('utf-8')
            total_bytes_rcv += document_len

        elif code == BIRTHDATE_CODE:
            birthdate_len = int.from_bytes(bet_info[total_bytes_rcv:INT32_LEN], byteorder='big') 
            total_bytes_rcv += INT32_LEN
            birthdate = bet_info[total_bytes_rcv:birthdate_len].decode('utf-8')
            total_bytes_rcv += birthdate_len

        elif code == NUMBER_CODE:
            number = int.from_bytes(bet_info[total_bytes_rcv:INT32_LEN], byteorder='big')
            total_bytes_rcv += INT32_LEN

    return name, surname, document, birthdate, number


