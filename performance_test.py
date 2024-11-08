import socket
import threading
import time
import matplotlib.pyplot as plt

# Server IP and port
SERVER_IP = '127.0.0.1'  # Change to your server IP if needed
SERVER_PORT = 8000

# Test parameters
NUM_CLIENTS = [1, 5, 10, 20, 50, 100]  # Number of clients to test
REQUESTS_PER_CLIENT = 10  # Number of requests each client will send


# Function to simulate a client sending requests to the server
def simulate_client(client_id, response_times):
    try:
        for _ in range(REQUESTS_PER_CLIENT):
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_IP, SERVER_PORT))

            # Measure the time to send a GET request and receive a response
            start_time = time.time()

            # Send a sample GET request
            request = f"GET /sample.txt {SERVER_IP}\r\n".encode('utf-8')
            client_socket.send(request)

            # Receive the response
            response = client_socket.recv(2048)
            end_time = time.time()

            # Record response time
            response_times.append(end_time - start_time)

            client_socket.close()
    except Exception as e:
        print(f"[Client {client_id}] Error: {e}")


# Function to run the performance test and gather data
def run_performance_test():
    all_results = []

    for num_clients in NUM_CLIENTS:
        print(f"Testing with {num_clients} clients...")

        threads = []
        response_times = []

        # Start multiple client threads
        for i in range(num_clients):
            thread = threading.Thread(target=simulate_client, args=(i, response_times))
            thread.start()
            threads.append(thread)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Calculate average response time
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        print(f"Average response time with {num_clients} clients: {avg_response_time:.4f} seconds")

        all_results.append((num_clients, avg_response_time))

    return all_results


# Function to plot the results
def plot_results(results):
    clients, response_times = zip(*results)
    plt.figure(figsize=(10, 6))
    plt.plot(clients, response_times, marker='o')
    plt.title("Server Response Time vs Number of Clients")
    plt.xlabel("Number of Clients")
    plt.ylabel("Average Response Time (seconds)")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    results = run_performance_test()
    plot_results(results)
