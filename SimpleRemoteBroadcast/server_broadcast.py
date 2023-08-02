import socket
import threading

connected_clients = []
client_lock = threading.Lock()

def broadcast(message, sender_conn):
    with client_lock:
        for client_conn in connected_clients:
            if client_conn != sender_conn:
                try:
                    client_conn.send(message.encode())
                except:
                    # If there's an error sending to a client, they might have disconnected
                    print("Error sending message to a client.")
                    client_conn.close()
                    connected_clients.remove(client_conn)

def handle_client_connection(conn, address):
    print("Connection from: " + str(address))
    with client_lock:
        connected_clients.append(conn)

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            message = f"from {address}: {data}"
            print(message)
            broadcast(message, conn)
    except:
        print("Client connection lost.")
    finally:
        with client_lock:
            connected_clients.remove(conn)
            conn.close()
            print("User " + str(address) + " has disconnected.")

def server_program():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        conn, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client_connection, args=(conn, address))
        client_thread.start()

if __name__ == '__main__':
    server_program()

