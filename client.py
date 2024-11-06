import socket
import os
import sys


def send_get_request(file_path_on_server, host_name):
    return f"GET {file_path_on_server} {host_name}\r\n".encode('utf-8')


def send_post_request(file_path_on_client, host_name):
    return f"POST /{file_path_on_client} {host_name}\r\n".encode('utf-8')


def run_client(server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    print(f"[C] Connected to server at {server_ip}:{server_port}")

    while True:
        command = input("Enter command or 'exit' to close: ")
        if command.lower() == 'exit':
            print(f"[C] Connection at client {server_ip}:{server_port} closed.")
            break

        parts = command.strip().split()
        if len(parts) < 2:
            print("[C] Invalid command format. Example: client_get file-path")
            continue

        command_type = parts[0]
        file_path = parts[1]

        if command_type == 'client_get':
            request = send_get_request(file_path, server_ip) #file path on server
            client.send(request)

            # Receive the file data from server and save it
            response = client.recv(2048).decode('utf-8')
            print(f"[C] Received response: {response}")
            if '404 Not Found' in response:
                print("[C] File not found on server.")

            else:
                # Save the file content
                file_name = os.path.basename(file_path)

                # Separate headers from the body
                header_end = response.find('\r\n\r\n') + 4
                body = response[header_end:]

                with open(file_name, 'w') as f:
                    f.write(body)
                    while True:
                        response = client.recv(2048)
                        if not response:
                            break
                        f.write(response)
                print(f"[C] File '{file_name}' received and saved.")

        elif command_type == 'client_post':
            # Ensure the file exists locally
            if not os.path.isfile(file_path):
                print(f"[C] File '{file_path}' not found locally.")
                continue

            request = send_post_request(file_path, server_ip)
            client.send(request)

            # Read file data and send to server
            with open(file_path, 'rb') as f:
                while (file_data := f.read(1024)):
                    client.send(file_data)
            print(f"[C] File '{file_path}' uploaded to server.")

    client.close()
    print("[C] Connection closed")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./my_client server_ip port_number")
        sys.exit(1)
    server_ip = sys.argv[1]
    if len(sys.argv) == 3:
        server_port = int(sys.argv[2])
    run_client(server_ip, server_port)