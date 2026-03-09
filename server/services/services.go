package services

import (
	"fmt"
	"net"
	"server/protocol"
	"sync"
)

const (
	OpenAccount uint16 = 0
	CloseAccount uint16 = 1
	CheckBalance uint16 = 2
	ChangePassword uint16 = 3
	DepositWithdraw uint16 = 4
	Monitor uint16 = 5
)

type HandlerFunc func(conn net.PacketConn, addr net.Addr, pkt *protocol.Packet) // <--- all function signature should follow
type User struct {
	name string
	password string
	currency int
	balance int
}
type Store struct {
	mu sync.RWMutex
	users map[string]*User // key:  account no. | value: user
}
type Services struct {
	Store *Store
	// ** add cache here
}
func NewServices() *Services {
	store := &Store{users: make(map[string]*User)}
	s := &Services{
		Store: store,
	}
	s.registerHandlers()
	return s
}

var handlers = make([]HandlerFunc, 6) // max of 6 operations
func (s *Services) registerHandlers() {
	// add handlers here
	// eg. handlers[OpenAccount] = s.handleOpenAccount <-- function pointer
}

func (s *Services) Handle(conn net.PacketConn, addr net.Addr, pkt *protocol.Packet) error {
	if pkt.SvcType > uint16(len(handlers)) {
		return fmt.Errorf("service type not found")
	}
	handlers[pkt.SvcType](conn, addr, pkt)
	return nil;
}