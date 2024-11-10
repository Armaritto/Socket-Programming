# Client-Server File Transfer

## Overview

This project implements a simple client-server file transfer system using sockets in Python. The server can handle multiple clients concurrently, allowing them to upload and download files. The client can send `GET` and `POST` requests to the server to retrieve and upload files, respectively.

## Algorithm

### Server

1. **Initialization**:
    - The server initializes a socket and binds it to a specified port.
    - It listens for incoming connections.

2. **Handling Connections**:
    - For each incoming connection, the server spawns a new thread to handle the client.
    - The server maintains a count of active connections and adjusts the timeout for each client based on the number of active connections.

3. **Processing Requests**:
    - The server reads the request from the client and parses the command (`GET` or `POST`).
    - For `GET` requests, the server reads the requested file and sends it back to the client.
    - For `POST` requests, the server receives the file data from the client and saves it to the local filesystem.

### Client

1. **Initialization**:
    - The client initializes a socket and connects to the server.
    - It receives the timeout value from the server.

2. **Sending Requests**:
    - The client reads commands from the user (`client_get` or `client_post`).
    - For `client_get`, the client sends a `GET` request to the server and saves the received file.
    - For `client_post`, the client sends a `POST` request along with the file data to the server.

## Data Structures

### Server

- **Socket**: Used to accept incoming connections and communicate with clients.
- **Thread**: Each client connection is handled in a separate thread.
- **Lock**: Used to safely update the count of active connections.

### Client

- **Socket**: Used to connect to the server and send/receive data.

## Performance Testing

The performance of the server is tested using a script (`performance_test.py`) that simulates multiple clients sending requests concurrently. The script measures the response time for each request and plots the average response time against the number of clients.

### Performance Test Script

1. **Simulate Clients**:
    - The script spawns multiple threads, each simulating a client sending requests to the server.

2. **Measure Response Time**:
    - For each request, the script measures the time taken to send the request and receive the response.

3. **Plot Results**:
    - The script plots the average response time against the number of clients using `matplotlib`.

## Usage

### Running the Server

```sh
python server.py [port]
```

### Running the Client

```sh
python client.py <server_ip> <server_port>
```

### Running the Performance Test
    
```sh
python performance_test.py
```
### Dependencies
- Python 3
- matplotlib (for testing)

## License
Save this content in a file named `README.md` in your project directory.