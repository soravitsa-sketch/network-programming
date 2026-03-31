# subscriber.py
import socket
import struct
import sys
from config import PORT, BUFFER_SIZE
from topics import TOPIC_CHANNELS
from utils.protocol import decode_message

def subscribe(topic):
    if topic not in TOPIC_CHANNELS:
        print(f"[ERROR] Topic '{topic}' not found.")
        return

    multicast_group = TOPIC_CHANNELS[topic]
    
    # สร้าง UDP Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    
    # อนุญาตให้หลายๆ โปรแกรมในเครื่องเดียวกันใช้ Port นี้พร้อมกันได้
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", PORT))

    # Join Multicast Group ตาม IP ของ Topic ที่เลือก
    mreq = struct.pack("4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"[*] Subscribed to [{topic}] -> Listening on {multicast_group}:{PORT}...")

    try:
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            msg = decode_message(data)
            print(f"[{msg['topic']}] from {addr[0]}: {msg['payload']}")
    except KeyboardInterrupt:
        print(f"\n[*] Leaving [{topic}] group. Goodbye!")
    finally:
        sock.close()

if __name__ == "__main__":
    # ตรวจสอบการใส่ Argument
    if len(sys.argv) < 2:
        print("Usage: python subscriber.py <TOPIC>")
        print(f"Available topics: {', '.join(TOPIC_CHANNELS.keys())}")
        sys.exit(1)
    
    topic_choice = sys.argv[1].upper()
    subscribe(topic_choice)