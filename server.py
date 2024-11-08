import socket
import os
import threading
import sys

def handle_client_connection(client_socket):
    while True:
        request = client_socket.recv(2048).decode('utf-8')
        if not request:
            break

        print(f"[*] Received:\n{request}")
        headers = request.split('\r\n')
        command_line = headers[0]
        command = command_line.split(' ')[0]
        file_path = command_line.split(' ')[1]

        if command == 'POST':
            content_length = 0
            for header in headers:
                if header.startswith('Content-Length: '):
                    content_length = int(header.split(' ')[1])
                    break

            if content_length == 0:
                print("[*] Received an empty file.")
                response = 'HTTP/1.1 200 OK\r\n\r\n'.encode('utf-8')
                client_socket.send(response)
                continue

            file_data = b''
            while len(file_data) < content_length:
                packet = client_socket.recv(2048)
                if not packet:
                    break
                file_data += packet

            file_name = file_path.split('/')[-1]
            file_path = os.path.dirname(__file__) + '/' + file_name
            with open(file_path, 'wb') as f:
                f.write(file_data)
            response = 'HTTP/1.1 200 OK\r\n\r\n'.encode('utf-8')
            client_socket.send(response)

    client_socket.close()

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[*] Listening on port {port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client_connection, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        port = 8081
    else:
        port = int(sys.argv[1])
    start_server(port)

