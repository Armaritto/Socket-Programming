import socket

def run_client(server_ip = '127.0.0.1',server_port = 8000):
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, server_port))
        print(f"[C] Connected to server at {server_ip}:{server_port}")
        while True:
            message = input("Enter message to send: ")
            client.send(message.encode('utf-8'))
            if message == 'close':
                break
            response = client.recv(1024).decode('utf-8')
            print(f"[C] Received from server: {response}")
    except Exception as e:
        print(f"[C] Error when running client: {e}")
    finally:
        client.close()
        print("[C] Connection closed")

if __name__ == '__main__':
    run_client()