import socket
import threading
import ssl

connected_clients = []
client_lock = threading.Lock()

def broadcast(message, sender_conn):
    with client_lock:
        for client_conn in connected_clients:
            if client_conn != sender_conn:
                try:
                    # Use the SSL-wrapped socket to send the message
                    client_conn.send(message.encode())
                except Exception as e:
                    print("Error sending message to a client:", str(e))
                    traceback.print_exc()
                    client_conn.close()
                    connected_clients.remove(client_conn)

def wrap_with_tls(conn):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    
    # Disable client-side certificate verification by setting cert_reqs to ssl.CERT_NONE
    context.verify_mode = ssl.CERT_NONE
    
    # context.verify_mode = ssl.CERT_REQUIRED
    # context.load_verify_locations(cafile=path_to_ca_cert)
    
    # Set the paths to your server's certificate and private key files
    server_certfile = './server.crt'
    server_keyfile = './server.key'
    context.load_cert_chain(certfile=server_certfile, keyfile=server_keyfile)

    return context.wrap_socket(conn, server_side=True)


def handle_client_connection(conn, address):
	print("Connection from: " + str(address))
	try:
		conn = wrap_with_tls(conn) # Wrap the connection with TLS encryption
		
		with client_lock: # IMPORTANT: Add wrapped SSL sockets to connected_client list
			connected_clients.append(conn)
			
		while True:
			data = conn.recv(1024).decode()
			if not data:
				break
			message = f"from {address}: {data}"
			print(message)
			broadcast(message, conn)
	except:
		print("Client",  str(address), "connection lost.")
	finally:
		with client_lock:
			if conn in connected_clients:  # Check if the client connection is still in the list
				connected_clients.remove(conn)
			conn.close()
			print("User " + str(address) + " has disconnected.")






def server_program():
    host = socket.gethostname()
    port = 5003

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
