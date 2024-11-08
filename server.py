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


        file_type = file_path.split('.')[-1]
        if file_type == 'txt':
            file_type = 'text/plain'
        elif file_type == 'jpeg':
            file_type = 'image/jpeg'
        elif file_type == 'html':
            file_type = 'text/html'

        if command == 'GET':
            if os.path.isfile(file_path):
                if file_type == 'text/plain':
                    with open(file_path, 'r') as f:
                        print(f"[*] Reading file {file_path}")
                        file_data = f.read().encode('utf-8')
                        print(f"[*] Finished reading file {file_path}")
                else:
                    with open(file_path, 'rb') as f:
                        print(f"[*] Reading file {file_path}")
                        file_data = f.read()
                        print(f"[*] Finished reading file {file_path}")
                print(f"[*] Sending file {file_path}")
                response = f'HTTP/1.1 200 OK\r\nContent-Type: {file_type}\r\nContent-Length: {len(file_data)}\r\n\r\n'.encode(
                    'utf-8') + file_data
                print(f"[*] Finished sending file {file_path}")
            else:
                response = 'HTTP/1.1 404 Not Found\r\n\r\n'.encode('utf-8')
            client_socket.send(response)
            print(f"[*] Finished sending response")

        elif command == 'POST':
            content_length = 0
            for header in headers:
                if header.startswith('Content-Length: '):
                    content_length = int(header.split(' ')[1])
                    break

            file_data = client_socket.recv(content_length)
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
        port = 80
    else:
        port = int(sys.argv[1])
    start_server(port)

