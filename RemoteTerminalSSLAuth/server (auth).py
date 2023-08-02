import socket
import threading
import ssl

connected_clients = []
client_lock = threading.Lock()

# dictionary to store valid usernames and their passwords
valid_users = {
    "user1": "1",
    "user2": "2"
}


# Color for terminal
RED='\033[0;31m'
NC='\033[0m' # No Color


def broadcast(message, sender_conn):
    with client_lock:
        for client_conn in connected_clients:
            if client_conn != sender_conn:
                try:
                    # Use the SSL-wrapped socket to send the message
                    client_conn.send(message.encode())
                except Exception as e:
                    print("Error sending message to a client:", str(e))
                    client_conn.close()
                    connected_clients.remove(client_conn)

def wrap_with_tls(conn):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    
    # Disable client-side certificate verification by setting cert_reqs to ssl.CERT_NONE
    context.verify_mode = ssl.CERT_NONE
    
    # context.verify_mode = ssl.CERT_REQUIRED
    # context.load_verify_locations(cafile=path_to_ca_cert)
    
    # Set the paths to your server's certificate and private key files
    server_certfile = '/home/userd/Desktop/certificate/server.crt'
    server_keyfile = '/home/userd/Desktop/certificate/server.key'
    context.load_cert_chain(certfile=server_certfile, keyfile=server_keyfile)

    return context.wrap_socket(conn, server_side=True)

def handle_client_connection(conn, address):
    print("Connection from: " + str(address))

    
    try:
        conn = wrap_with_tls(conn)  # Wrap the connection with TLS encryption

		# Authenticate the client
        credentials = conn.recv(1024).decode().strip()
        print(credentials)
        username, password = credentials.split(":")  # Split the credentials string

        # Check if the provided username and password match the valid users
        if username in valid_users and valid_users[username] == password:
            conn.send("authenticated".encode())
            print(f"User {username} authenticated.")
        else:
            conn.send("unauthorized".encode())
            print(f"User {username} authentication failed. Closing the connection.")
            conn.close()
            return

        with client_lock:  # IMPORTANT: Add wrapped SSL sockets to connected_client list
            connected_clients.append(conn)

        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            message = f"From {RED} {address} {username}{NC}: {data}"
            print(message)
            broadcast(message, conn)
    except Exception as e:
        print("Client", str(address), "connection lost:", str(e))
    finally:
        with client_lock:
            if conn in connected_clients:  # Check if the client connection is still in the list
                connected_clients.remove(conn)
            conn.close()
            print("User " + str(address) + " has disconnected.")

def server_program():
    host = socket.gethostname()
    port = 5001

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Server is listening on {}:{}".format(host, port))

    while True:
        conn, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client_connection, args=(conn, address))
        client_thread.start()

if __name__ == '__main__':
    server_program()
