import socket
import os
import sys
import time

def send_get_request(file_path_on_server, host_name):
    return f"GET {file_path_on_server} HTTP/1.1\r\nHost: {host_name}\r\n\r\n".encode('utf-8')

def send_post_request(file_path_on_client, host_name, file_size):
    return f"POST /{file_path_on_client} HTTP/1.1\r\nHost: {host_name}\r\nContent-Length: {file_size}\r\n\r\n".encode('utf-8')

def run_client(server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    print(f"[C] Connected to server at {server_ip}:{server_port}")

    # Receive timeout value from server
    timeout_message = client.recv(1024).decode('utf-8')
    if "Timeout" in timeout_message:
        timeout = float(timeout_message.split(": ")[1])
        print(f"[C] Server assigned timeout: {timeout} seconds")
    else:
        print("[C] No timeout received from server.")
        timeout = 60  # Default timeout if not provided

    last_activity = time.time()

    while True:
        try:
            # Calculate time since last activity
            if time.time() - last_activity >= timeout:
                print(f"[C] No activity for {timeout} seconds. Closing connection.")
                break

            command = input("Enter command or 'exit' to close: ")
            if command.lower() == 'exit':
                print(f"[C] Closing client connection.")
                break

            parts = command.strip().split()
            if len(parts) < 2:
                print("[C] Invalid command format. Example: client_get file-path")
                continue

            command_type = parts[0]
            file_path = parts[1]

            if command_type == 'client_get':
                request = send_get_request(file_path, server_ip)
                client.send(request)
                response = client.recv(2048)

                if b'Connection: close' in response:
                    print("[C] Server is closing the connection.")
                    break

                print(f"[C] Received response:\n{response.decode('utf-8')}")
                last_activity = time.time()  # Update last activity time after each successful request
        except ConnectionAbortedError:
            print("[C] Closed connection due to timeout")
            client.close()
            sys.exit(1)
    client.close()
    print("[C] Connection closed.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./my_client server_ip port_number")
        sys.exit(1)
    server_ip = sys.argv[1]
    if len(sys.argv) == 3:
        server_port = int(sys.argv[2])
    run_client(server_ip, server_port)