package common

import (
	"bufio"
	"net"
	"os"
	"time"

	"strconv"
	"strings"

	"github.com/op/go-logging"
)

const MAX_MESSAGE_SIZE = 8192

var log = logging.MustGetLogger("log")

// ClientConfig Configuration used by the client
type ClientConfig struct {
	ID            string
	ServerAddress string
	LoopAmount    int
	LoopPeriod    time.Duration
	BatchMaxAmount int
}

// Client Entity that encapsulates how
type Client struct {
	config ClientConfig
	conn   net.Conn
}

// NewClient Initializes a new client receiving the configuration
// as a parameter
func NewClient(config ClientConfig) *Client {
	client := &Client{
		config: config,
	}
	return client
}

// CreateClientSocket Initializes client socket. In case of
// failure, error is printed in stdout/stderr and exit 1
// is returned
func (c *Client) createClientSocket() error {
	conn, err := net.Dial("tcp", c.config.ServerAddress)
	if err != nil {
		log.Criticalf(
			"action: connect | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
	}
	c.conn = conn
	return nil
}

// StartClientLoop Send messages to the client until some time threshold is met
func (c *Client) StartClientLoop() {
	// There is an autoincremental msgID to identify every message sent
	// Messages if the message amount threshold has not been surpassed

	c.createClientSocket()

	id, _ := strconv.Atoi(c.config.ID)
	// file := fmt.Sprintf("./agency-%d.csv", id)

	f, err := os.Open("./agency.csv")

	if err != nil {
		log.Criticalf("action: open_file | result: fail | client_id: %v | error: %v", c.config.ID, err)
	}

	defer f.Close()

	scanner := bufio.NewScanner(f)

	bets_raw := []byte{}
	batchNum := 0


	for scanner.Scan() {
		line := scanner.Text()

		bet_arr := strings.Split(line, ",")

		bet := Bet{
			Name:      bet_arr[0],
			Surname:   bet_arr[1],
			Id:        bet_arr[2],
			Birthdate: bet_arr[3],
			Number:    bet_arr[4],
		}

		encodedBet := EncodeBet(bet)

		if len(bets_raw) + len(encodedBet) < MAX_MESSAGE_SIZE {
			bets_raw = append(bets_raw, encodedBet...)
		}

		batchNum++

		if batchNum == c.config.BatchMaxAmount {
			c.sendAll(FinalizeBet(bets_raw, int8(id)))
			c.getServerResponse()
			batchNum = 0
			bets_raw = []byte{}
		}

		time.Sleep(c.config.LoopPeriod)	
	}

	if len(bets_raw) > 0 {
		c.sendAll(FinalizeBet(bets_raw, int8(id)))
		time.Sleep(c.config.LoopPeriod)
	}

	c.Close()
	log.Infof("action: loop_finished | result: success | client_id: %v", c.config.ID)
}

func (c *Client) sendAll(data []byte) {
	sentData := 0

	for sentData < len(data) {
		nSent, err := c.conn.Write(data[sentData:])
		if err != nil {
			log.Criticalf("action: send_all | result: fail | client_id: %v | error: %v", c.config.ID, err)
		}
		sentData += nSent
	}
}

func (c *Client) getServerResponse() {
	msg, err := bufio.NewReader(c.conn).ReadString('\n')

	if err != nil {
		log.Errorf("action: receive_message | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
		return
	}

	if msg != "ACK\n" {
		log.Errorf("action: receive_message | result: fail | client_id: %v | msg: %v",
			c.config.ID,
			msg,
		)
		return
	}
}

func (c *Client) Close() {
	log.Infof("action: close | result: success | client_id: %v", c.config.ID)
	c.sendAll(WriteConnectionClosed())
	c.conn.Close()
}