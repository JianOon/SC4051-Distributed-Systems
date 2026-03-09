import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 2222
BUFFER_SIZE = 1024

reqid = 2
svctype = 0

arr = bytearray()
byte_order = 'big'
arr.extend(reqid.to_bytes(4, byteorder=byte_order))
arr.extend(svctype.to_bytes(2, byteorder=byte_order))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto(arr, (SERVER_IP, SERVER_PORT))

data, _ = client_socket.recvfrom(BUFFER_SIZE)
print(f"Server response: {data.decode('utf-8')}")
client_socket.close()