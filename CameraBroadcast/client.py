import socket
import cv2
import pickle
import struct

def receive_video():
    host = socket.gethostname()  # Replace with your server IP address
    port = 5002

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    data = b""
    payload_size = struct.calcsize("Q")
    
    
    cv2.namedWindow("RECEIVING VIDEO", cv2.WINDOW_NORMAL)

    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)  # 4K
            if not packet:
                break
            data += packet

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)

        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)

        cv2.imshow("RECEIVING VIDEO", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    client_socket.close()
    cv2.destroyAllWindows()

def main():
    receive_video()

if __name__ == "__main__":
    main()
