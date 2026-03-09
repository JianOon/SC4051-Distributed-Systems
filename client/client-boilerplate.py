import socket

# --- Configuration Constants ---
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432
BUFFER_SIZE = 1024
TIMEOUT_SECONDS = 2.0
MAX_RETRIES = 3

class UDPClient:
    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        self.server_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(TIMEOUT_SECONDS)

    def send_message(self, message: str):
        """Sends a string message to the configured server."""
        try:
            self.packet_count += 1
            print(f"[{self.packet_count}] Sending to {self.server_address}...")
            
            self.sock.sendto(message.encode('utf-8'), self.server_address)
            
            # Wait for response
            data, server = self.sock.recvfrom(BUFFER_SIZE)
            return data.decode('utf-8')

        except socket.timeout:
            return "Error: Request timed out."
        except Exception as e:
            return f"Error: {e}"

    def send_with_retry(self, message: str, retries=MAX_RETRIES):
        """Sends a message and retries up to 'retries' times on timeout."""
        for attempt in range(1, retries + 1):
            try:
                print(f"Attempt {attempt}: Sending to {self.server_address}...")
                self.sock.sendto(message.encode('utf-8'), self.server_address)
                
                data, _ = self.sock.recvfrom(BUFFER_SIZE)
                return data.decode('utf-8')

            except socket.timeout:
                print(f"Attempt {attempt} timed out.")
                if attempt == retries:
                    return "Error: Maximum retries reached. Server unreachable."
        
    def close(self):
        self.sock.close()


if __name__ == "__main__":
    client = UDPClient()
    
    response = client.send_with_retry("Ping")
    print(f"Final Result: {response}")
    
    client.close()