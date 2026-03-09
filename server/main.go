package main

import (
	"log"
	"net"
	"server/protocol"
	"server/services"
)

type Service uint16

const (
	port = ":2222" // change to any port
)

func processPacket(conn net.PacketConn, addr net.Addr, data []byte, service *services.Services) {
	pkt, err := protocol.Decode(data)
	if err != nil {
		log.Printf(err.Error())
		return
	}
	err = service.Handle(conn, addr, pkt)
	if err != nil {
		log.Printf(err.Error())
		return
	}
}

func main() {
	// init server to listen for packets
	conn, err := net.ListenPacket("udp", port)
	if err != nil {
		log.Fatalf("UDP server failed to listen %s", err)
	}
	defer conn.Close()
	log.Printf("UDP server listening on %s", port)

	const maxPacketSize = 65535 // max udp size
	buffer := make([]byte, maxPacketSize)

	service := services.NewServices()

	// listening loop
	for {
		n, addr, err := conn.ReadFrom(buffer)
		if err != nil {
			log.Printf("read error: %s", err)
			continue
		}

		raw := make([]byte, n)
		copy(raw, buffer[:n])
		go processPacket(conn, addr, raw, service)
	}
}
