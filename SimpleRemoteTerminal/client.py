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
            # hsandle the case when no data is received (socket would raise EWOULDBLOCK)
            pass

def client_program():
    host = socket.gethostname()  # as both code is running on the same PC
    port = 5003  # socket server port number

    # Create an SSL context with appropriate SSL/TLS version (e.g., PROTOCOL_TLSv1_2)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    
    # Disable server-side certificate verification by setting cert_reqs to ssl.CERT_NONE
    # context.verify_mode = ssl.CERT_NONE

    # Set the client_certfile and client_keyfile to the path of your client's certificate and private key (if needed).
    # Optionally, set cert_reqs=ssl.CERT_REQUIRED and cafile to the path of a CA certificate bundle
    # to verify the server's certificate if required.
    # context.load_cert_chain(certfile=client_certfile, keyfile=client_keyfile)

    # Instantiate a socket with the SSL context
    client_socket = context.wrap_socket(socket.socket())

    try:
        client_socket.connect((host, port))  # connect to the server

        # set the socket to non-blocking mode
        client_socket.setblocking(False)

        # start a separate thread to continuously receive messages from the server
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        message = input("(Me): ")  # take input

        while message.lower().strip() != 'bye':
            if message:  # Check if the message is not empty. If message is empty  => ssl.SSLEOFError: EOF occurred in violation of protocol (_ssl.c:2483)
                client_socket.send(message.encode())  # send message
            message = input("(Me): ")   # again take input

    finally:
        client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()
