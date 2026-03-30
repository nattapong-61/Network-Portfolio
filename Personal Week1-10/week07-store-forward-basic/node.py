#Nattapong 673380038-9

import socket
import threading
import time
import sys
from config import HOST, BASE_PORT, BUFFER_SIZE, RETRY_INTERVAL
from message_queue import MessageQueue

if len(sys.argv) < 2:
    print("Usage: python node.py [ID]")
    sys.exit()

node_id = int(sys.argv[1])
MY_PORT = BASE_PORT + node_id
msg_queue = MessageQueue()


def start_receiver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, MY_PORT))
    sock.listen(5)
    print(f" [NODE {node_id}] ฟังอยู่ที่พอร์ต {MY_PORT}")
    while True:
        conn, addr = sock.accept()
        data = conn.recv(BUFFER_SIZE).decode()
        if data:
            print(f"\n [ได้รับ] จาก {addr}: {data}")
        conn.close()


def retry_worker():
    while True:
        pending_msgs = msg_queue.get_messages()
        for item in pending_msgs:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((HOST, item['peer']))
                s.sendall(item['message'].encode())
                s.close()
                print(f"[RETRY SUCCESS] ส่งข้อความค้างคาไปที่ {item['peer']} สำเร็จ!")
                msg_queue.remove_message(item)
            except:
               
                pass
        time.sleep(RETRY_INTERVAL)


threading.Thread(target=start_receiver, daemon=True).start()
threading.Thread(target=retry_worker, daemon=True).start()


print(f" Welcome Node {node_id} Store-and-Forward")
while True:
    target_port = input("\nใส่พอร์ตเพื่อนที่จะส่ง (เช่น 8001) หรือ 'exit': ")
    
   
    if not target_port.strip():
        continue
        
    if target_port.lower() == 'exit': 
        break
    
    msg = input("พิมพ์ข้อความ: ")
    full_msg = f"จาก Node {node_id}: {msg}"
    
    try:

        p = int(target_port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((HOST, p))
        s.sendall(full_msg.encode())
        s.close()
        print(" [DIRECT SENT] ส่งถึงมือเพื่อนทันที")
    except ValueError:
        print("กรุณาใส่เฉพาะตัวเลขพอร์ตเท่านั้น")
    except:
        
        print(f"[STORED] ติดต่อพอร์ต {target_port} ไม่ได้... ฝากข้อความไว้รอส่งใหม่")
        msg_queue.add_message(full_msg, int(target_port))