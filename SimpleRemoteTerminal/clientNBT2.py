import socket
import ssl
import threading


def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()  # receive response
            if data:
                print('Received from server:', data)  # show in terminal
        except socket.error as e:
            # Handle the case when no data is received (socket would raise EWOULDBLOCK)
            pass

def send_message(client_socket, message):
    if message:  # Check if the message is not empty
        client_socket.send(message.encode())  # send message

def handle_user_input(client_socket):

    message = ""  # Initialize the message variable as an empty string

    while not message:  # Keep looping until the user provides some input (non-empty string)
        message = input("(Me): ")


    while message.lower().strip() != 'bye':
        send_message(client_socket, message)
        message = input("(Me): ")  # again take input

def client_program():
    host = socket.gethostname()  # as both code is running on the same PC
    port = 5003  # socket server port number

    # Create an SSL context with appropriate SSL/TLS version (e.g., PROTOCOL_TLSv1_2)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

    # Instantiate a socket with the SSL context
    client_socket = context.wrap_socket(socket.socket())

    try:
        client_socket.connect((host, port))  # connect to the server

        # Set the socket to non-blocking mode
        client_socket.setblocking(False)

        # Start a separate thread to continuously receive messages from the server
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        # Start another thread to handle user input and sending messages
        input_thread = threading.Thread(target=handle_user_input, args=(client_socket,))
        input_thread.start()

        # Wait for both threads to finish (this will never happen as they run indefinitely)
        receive_thread.join()
        input_thread.join()

    finally:
        client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()

