import socket

# client
def run_client(server_ip="127.0.0.1", port_number=8000):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #server ip and port
    server_port = port_number

    #establish connection
    client.connect((server_ip, server_port))

    while True:
        #send message
        message = input("Enter your message: ")
        client.send(message.encode("utf-8")[:1024])

        #receive message
        response = client.recv(1024)
        response = response.decode("utf-8")
        print("Received from server: ", response)

        if response.lower() == "close":
            break

    client.close()
    print("Connection to Server Closed")

run_client()
