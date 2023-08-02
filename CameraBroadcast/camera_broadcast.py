import socket
import cv2
import pickle
import struct
import imutils

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('Hosting at:', host_ip)
port = 5002
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("Listing on:", socket_address)

def send_video(client_socket):
    vid = cv2.VideoCapture(0)

    while True:
        # Capture the frame from the camera
        ret, frame = vid.read()
        if not ret:
            print("No frame from the camera.")
            break

        # Serialize the frame
        data = pickle.dumps(frame)

        # Pack the serialized frame into a message with a header indicating its length
        message = struct.pack("Q", len(data)) + data

        try:
            # Send the message with the frame to the client
            client_socket.sendall(message)

            # transmitting frame
            # cv2.imshow('TRANSMITTING VIDEO', frame)

            # Check for the 'q' key press to stop transmitting
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        except socket.error:
            print("Client disconnected.")
            break

    # release the video capture and close any OpenCV windows
    vid.release()
    cv2.destroyAllWindows()

def main():
    while True:
        try:
            client_socket, addr = server_socket.accept()
            print('GOT CONNECTION FROM:', addr)
            send_video(client_socket)
        except KeyboardInterrupt:
            print("Server interrupted.")
            break

    server_socket.close()

if __name__ == "__main__":
    main()
