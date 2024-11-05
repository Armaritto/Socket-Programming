import socket
import threading

def handle_client(client_socket, addr):
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if request == 'close':
                client_socket.send('Connection closed'.encode('utf-8'))
                break
            print(f"[*] Received: {request}")
            response = "accepted"
            client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"[*] Error when handling client: {e}")
    finally:
        client_socket.close()
        print(f"[*] Connection closed with {addr}")

def run_server():
    server_ip = '127.0.0.1'
    server_port = 8000
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip, server_port))
        server.listen()
        print(f"[*] Server is listening on {server_ip}:{server_port}")
        while True:
            client_socket, addr = server.accept()
            print(f"[*] Connection established with {addr}")
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
    except Exception as e:
        print(f"[*] Error when running server: {e}")
    finally:
        server.close()

if __name__ == '__main__':
    run_server()