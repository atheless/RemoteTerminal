import socket

def client_program():
    host = socket.gethostname()  # as both code is running on the same PC
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    # Set the socket to non-blocking mode
    client_socket.setblocking(False)

    message = input(" -> ")  # take input

    while message.lower().strip() != 'exit':
        client_socket.send(message.encode())  # send message

        try:
            data = client_socket.recv(1024).decode()  # receive response
            if data:
                print('Received from server: ' + data)  # show in terminal
        except socket.error as e:
            # Handle the case when no data is received (socket would raise EWOULDBLOCK)
            pass

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()
