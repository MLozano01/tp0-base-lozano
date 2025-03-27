package common

import (
	"bytes"
	"encoding/binary"


)

const (
	NAME_CODE = 1
	SURNAME_CODE = 2
	ID_CODE = 3
	BIRTHDATE_CODE = 4
	NUMBER_CODE = 5
	END_BET = 6

)

const(
	BET = 1
	CLOSED = 2
	INFO = 3
	DONE = 4
	ACK = "ACK\n"
	ERROR = "ERROR\n"
	WINNER = "WINNERS\n"
	NO_WINNER = "NO_WINNERS\n"
)

// Protocol 
// 0. Total length (int32)
// 0. Content (int8)
// 0. Agency (int8)
// 1. NAME_CODE (int8) | length (int16) | name (string)
// 2. SURNAME_CODE (int8) | length (int16) | surname (string)
// 3. ID_CODE (int8) | length (int16) | surname (string)
// 4. BIRTHDATE_CODE (int8) | length (int16) | birthdate (string)
// 5. NUMBER_CODE (int8) | length (int16) | number (string)
// 6. End of Bet (ini8)

func EncodeBet(bet Bet) []byte {

	buf := new(bytes.Buffer)

	writeString(buf, bet.Name, NAME_CODE)

	writeString(buf, bet.Surname, SURNAME_CODE)

	writeString(buf, bet.Id, ID_CODE)

	writeString(buf, bet.Birthdate, BIRTHDATE_CODE)

	writeString(buf, bet.Number, NUMBER_CODE)

	err := binary.Write(buf, binary.BigEndian, int8(END_BET))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	return buf.Bytes()
}

func FinalizeBet(bets []byte, agency int8) []byte {
	final_bets := new(bytes.Buffer)

	err := binary.Write(final_bets, binary.BigEndian, int32(len(bets) + 2))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	err =  binary.Write(final_bets, binary.BigEndian, int8(BET))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	err = binary.Write(final_bets, binary.BigEndian, agency)

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	final_bets.Write(bets)

	return final_bets.Bytes()
}

func WriteConnectionClosed() []byte {
	buf := new(bytes.Buffer)

	err := binary.Write(buf, binary.BigEndian, int32(1))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	err = binary.Write(buf, binary.BigEndian, int8(CLOSED))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	return buf.Bytes()
}

func writeString(buf *bytes.Buffer, s string, code int) {

	err := binary.Write(buf, binary.BigEndian, int8(code))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	err = binary.Write(buf, binary.BigEndian, int16(len(s)))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}
	_, err = buf.WriteString(s)

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}
}

func SendClientInfo(agency int8) []byte {
	buf := new(bytes.Buffer)

	err := binary.Write(buf, binary.BigEndian, int32(2))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	err = binary.Write(buf, binary.BigEndian, int8(INFO))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	err = binary.Write(buf, binary.BigEndian, agency)

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	return buf.Bytes()
}

func SendClientDone() []byte {
	buf := new(bytes.Buffer)

	err := binary.Write(buf, binary.BigEndian, int32(1))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	err = binary.Write(buf, binary.BigEndian, int8(DONE))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	return buf.Bytes()
}
