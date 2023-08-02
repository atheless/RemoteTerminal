import socket
import threading


connected_users = []  # global list to store connected user pool




def handle_client_connection(conn, address):
		connected_users.append(address)  # Add the new client's address to the list
    print("New connection from: " + str(address))

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from "+ str(address) + ":"+ str(data))
        # data = input(' -> ') # Comment for non-blocking
        # conn.send(data.encode()) # Comment for non-blocking


    connected_users.remove(address)  # remove the client's address from the list
		print("User " + str(address) + " has disconnected.")
    conn.close()

def server_program():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2) #  max queue size

    while True:
        conn, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client_connection, args=(conn, address))
        client_thread.start()

if __name__ == '__main__':
    server_program()
