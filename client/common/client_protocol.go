package common

import (
	"bytes"
	"encoding/binary"

)

const (
	NAME_CODE = 01
	SURNAME_CODE = 02
	ID_CODE = 03
	BIRTHDATE_CODE = 04
	NUMBER_CODE = 05
)

// Protocol 
// 0. Total length (int32)
// 1. NAME_CODE (int32) | length (int32) | name (string)
// 2. SURNAME_CODE (int32) | length (int32) | surname (string)
// 3. ID_CODE (int32) | length (int32) | surname (string)
// 4. BIRTHDATE_CODE (int32) | length (int32) | birthdate (string)
// 5. NUMBER_CODE (int32) | number (int32)

func EncodeBet(bet Bet) []byte {

	buf := new(bytes.Buffer)

	writeString(buf, bet.Name, NAME_CODE)

	writeString(buf, bet.Surname, SURNAME_CODE)

	writeString(buf, bet.Id, ID_CODE)

	writeString(buf, bet.Birthdate, BIRTHDATE_CODE)

	writeInt32(buf, bet.Number, NUMBER_CODE)

	final_bets := new(bytes.Buffer)

	err := binary.Write(final_bets, binary.BigEndian, int32(len(buf.Bytes())))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	final_bets.WriteTo(buf)

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

func writeInt32(buf *bytes.Buffer, num int32, code int) {
	
	err := binary.Write(buf, binary.BigEndian, int32(code))

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}

	err = binary.Write(buf, binary.BigEndian, num)

	if err != nil {
		log.Criticalf("action: encode_bet | result: fail | error: %v", err)
	}
}
