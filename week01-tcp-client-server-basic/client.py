#Nattapong 673380038-9
import socket
from config import HOST, PORT, BUFFER_SIZE

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.settimeout(5.0) 

try:
    client_socket.connect((HOST, PORT))
    
    message = "Hello gay"
    client_socket.sendall(message.encode())

    response = client_socket.recv(BUFFER_SIZE)
    print(f"[CLIENT] Received: {response.decode()}")

except socket.timeout:
    print("[CLIENT ERROR] Server นานเกินไป (Timeout!)")
except Exception as e:
    print(f"[CLIENT ERROR] เกิดข้อผิดพลาด: {e}")
finally:
    client_socket.close()
    print("[CLIENT] Closed connection")