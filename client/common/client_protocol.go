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

	CLOSED = "CLOSED\n"
)

// Protocol 
// 0. Total length (int32)
// 0. Agency (int32)
// 1. NAME_CODE (int32) | length (int32) | name (string)
// 2. SURNAME_CODE (int32) | length (int32) | surname (string)
// 3. ID_CODE (int32) | length (int32) | surname (string)
// 4. BIRTHDATE_CODE (int32) | length (int32) | birthdate (string)
// 5. NUMBER_CODE (int32) | number (int32)
// 6. End of Bet (int32)

func EncodeBet(bet Bet) []byte {

	buf := new(bytes.Buffer)

	writeString(buf, bet.Name, NAME_CODE)

	writeString(buf, bet.Surname, SURNAME_CODE)

	writeString(buf, bet.Id, ID_CODE)

	writeString(buf, bet.Birthdate, BIRTHDATE_CODE)

	writeString(buf, bet.Number, NUMBER_CODE)

	err := binary.Write(buf, binary.BigEndian, int32(END_BET))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	return buf.Bytes()
}

func FinalizeBet(bets []byte, agency int32) []byte {
	final_bets := new(bytes.Buffer)

	err := binary.Write(final_bets, binary.BigEndian, int32(len(bets)))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	err = binary.Write(final_bets, binary.BigEndian, agency)

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	final_bets.Write(bets)

	log.Infof("Finalize Bet: ", final_bets.Bytes())

	return final_bets.Bytes()
}

func WriteConnectionClosed() []byte {
	buf := new(bytes.Buffer)



	err := binary.Write(buf, binary.BigEndian, int32(len(CLOSED)))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	_, err = buf.WriteString(CLOSED)

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	return buf.Bytes()
}

func writeString(buf *bytes.Buffer, s string, code int) {

	err := binary.Write(buf, binary.BigEndian, int32(code))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	err = binary.Write(buf, binary.BigEndian, int32(len(s)))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}
	_, err = buf.WriteString(s)

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}
}

// func writeInt32(buf *bytes.Buffer, num int32, code int) {
	
// 	err := binary.Write(buf, binary.BigEndian, int32(code))

// 	if err != nil {
// 		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
// 	}

// 	err = binary.Write(buf, binary.BigEndian, num)

// 	if err != nil {
// 		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
// 	}
// }