package protocol
import (
	"fmt"
	"bytes"
	"encoding/binary"
)

const headerSize = 6;

// 6 byte header
type Header struct {
	ReqID uint32
	SvcType uint16
}

type Packet struct {
	Header
	Payload []byte
}

func Decode(data []byte) (*Packet, error) {
	if len(data) < headerSize {
		return nil, fmt.Errorf("packet too short, no header found")
	}
	// read bytes in big endian order
	reader := bytes.NewReader(data[:headerSize])
	var header Header
	err := binary.Read(reader, binary.BigEndian, &header)
	if err != nil {
		return nil, err
	}

	// decode packet into struct
	payload := make([]byte, len(data) - headerSize)
	copy(payload, data[headerSize:])
	return &Packet{
		Header: header,
		Payload: payload,
	}, nil
}

func (p *Packet) Encode() ([]byte, error) {
	// write packet into byte array
	buffer := new(bytes.Buffer)
	err := binary.Write(buffer, binary.BigEndian, p.Header)
	if err != nil {
		return nil, err
	}
	_, err = buffer.Write(p.Payload)
	if err != nil {
		return nil, err
	}
	return buffer.Bytes(), nil
}