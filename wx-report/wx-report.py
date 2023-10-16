import socket
import threading
import requests
import os
import argparse

# Define the default values for the arguments
DEFAULT_IP_ADDRESS = '127.0.0.1'
DEFAULT_PORT = 9000
DEFAULT_CITY = 'aylesbury'

# Create an argument parser
parser = argparse.ArgumentParser(description='A simple weather server')

# Add the arguments
parser.add_argument('-i', '--ip-address', type=str, default=os.getenv('IP_ADDRESS', DEFAULT_IP_ADDRESS),
                    help=f'the IP address to listen on (default: {os.getenv("IP_ADDRESS", DEFAULT_IP_ADDRESS)})')
parser.add_argument('-p', '--port', type=int, default=int(os.getenv('PORT', DEFAULT_PORT)),
                    help=f'the port number to listen on (default: {int(os.getenv("PORT", DEFAULT_PORT))})')
parser.add_argument('-c', '--city', type=str, default=os.getenv('CITY', DEFAULT_CITY),
                    help=f'the home city to get the weather for (default: {os.getenv("CITY", DEFAULT_CITY)})')

# Parse the arguments
args = parser.parse_args()


# Get the IP address, port number, and home city from the arguments or environment variables
IP_ADDRESS = os.getenv('IP_ADDRESS', args.ip_address)
PORT = int(os.getenv('PORT', args.port))
CITY = os.getenv('CITY', args.city).replace(" ", "+") # Replace whitespace for +

# Create a TCP socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the IP address and port number
server_socket.bind((IP_ADDRESS, PORT))

# Listen for incoming connections
server_socket.listen()

print(f"Server listening on {IP_ADDRESS}:{PORT}")

# Function to handle a single client connection
def handle_client(client_socket):
    print(f"New client connected: {client_socket.getpeername()}")

    # Fetch the content from the weather API for the home city
    home_response = get_weather(CITY)

    # Send the response for the home city to the client
    client_socket.sendall(home_response)

    # Counter for the number of iterations
    counter = 0

    while True:


        # Prompt the client to enter a new city name
        client_socket.sendall(b"Do you want to query the weather for another city? (Y/N)\n")
        response = client_socket.recv(1024).decode().strip().lower()

        if response == "n":
            break
        elif response == "y":
            client_socket.sendall(b"Please enter the city name:\n")
            city_name = client_socket.recv(1024).decode().strip().replace(" ", "+")

            # Fetch the content from the weather API for the new city
            response = get_weather(city_name)

            # Send the response to the client
            client_socket.sendall(response)

        # Increment the counter
        counter += 1

        # If the counter reaches 3, break out of the loop
        if counter == 3:
            client_socket.sendall(b"Goodbye!\n")
            break

    # Close the client socket
    client_socket.close()


# Function to accept new client connections
def accept_clients():
    while True:
        # Accept a new client connection
        client_socket, client_address = server_socket.accept()

        # Start a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


# Function to fetch the weather information from the API
def get_weather(city):
    try:
        response = requests.get(f"http://wttr.in/{city}?mTn2F")
        return response.content
    except requests.exceptions.RequestException:
        return b"There has been an error, please try again later\n"


# Start the thread to accept new client connections
accept_thread = threading.Thread(target=accept_clients)
accept_thread.start()

