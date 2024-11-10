import socket
import os
import threading
import sys


# Global variable to track active connections
active_connections = 0
lock = threading.Lock()  # To safely update the connection count

def calculate_timeout():
    """ Calculate timeout based on the number of active connections """
    base_timeout = 1800  # seconds
    with lock:
        t = base_timeout / (1 + active_connections)
    return max(t, 30)  # Ensure minimum timeout of 5 seconds


def handle_client_connection(client_socket):

    global active_connections


    with lock:
        active_connections += 1

    timeout = calculate_timeout()
    client_socket.settimeout(timeout)

    # Send the timeout value to the client
    client_socket.send(f"Timeout: {timeout}".encode('utf-8'))
    try:
        while True:
            try:
                request = client_socket.recv(2048).decode('utf-8')
                if not request:
                    break

                print(f"[S] Received:\n{request}")
                headers = request.split('\r\n')
                command_line = headers[0]
                command = command_line.split(' ')[0]
                file_path = command_line.split(' ')[1]


                file_type = file_path.split('.')[-1]
                if file_type == 'txt':
                    file_type = 'text'
                elif file_type == 'jpeg':
                    file_type = 'image'
                elif file_type == 'html':
                    file_type = 'html'

                if command == 'GET':
                    if os.path.isfile(file_path):
                        if file_type == 'text':
                            with open(file_path, 'r') as f:
                                print(f"[S] Reading file {file_path}")
                                file_data = f.read().encode('utf-8')
                                print(f"[S] Finished reading file {file_path}")
                        else:
                            with open(file_path, 'rb') as f:
                                print(f"[S] Reading file {file_path}")
                                file_data = f.read()
                                print(f"[S] Finished reading file {file_path}")
                        print(f"[S] Sending file {file_path}")
                        response = f'HTTP/1.1 200 OK\r\nContent-Type: {file_type}\r\nContent-Length: {len(file_data)}\r\n\r\n'.encode(
                            'utf-8') + file_data
                        print(f"[S] Finished sending file {file_path}")
                    else:
                        response = 'HTTP/1.1 404 Not Found\r\n\r\n'.encode('utf-8')
                    client_socket.send(response)
                    print(f"[S] Finished sending response")

                elif command == 'POST':
                    content_length = 0
                    for header in headers:
                        if header.startswith('Content-Length: '):
                            content_length = int(header.split(' ')[1])
                            break

                    if content_length == 0:
                        print("[S] Received an empty file.")
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


            except socket.timeout:
                print(f"[S] Client timed out after {timeout} seconds of inactivity")
                break
    finally:
        with lock:
            active_connections -= 1
        client_socket.close()
        print(f"[S] Connection closed. Active connections: {active_connections}")


def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen()
    print(f"[S] Listening on port {port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[S] Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client_connection, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        port = 8000
    else:
        port = int(sys.argv[1])
    start_server(port)

