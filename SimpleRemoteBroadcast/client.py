import socket
import threading

def receive_messages(client_socket):
    try:
        while True:
            data = client_socket.recv(1024).decode()
            print(data)
    except:
        print("Connection to server lost.")
        client_socket.close()

def client_program():
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        client_socket.send(message.encode())

if __name__ == '__main__':
    client_program()

