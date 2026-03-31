# publisher.py
import socket
import time
from config import PORT, TTL
from topics import TOPIC_CHANNELS
from utils.protocol import encode_message

def publish(topic, payload):
    # ตรวจสอบว่ามี Topic นี้ในระบบหรือไม่
    if topic not in TOPIC_CHANNELS:
        print(f"[ERROR] Topic '{topic}' not found.")
        return

    multicast_group = TOPIC_CHANNELS[topic]
    
    # สร้าง UDP Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)

    # แปลงและส่งข้อมูล
    data = encode_message(topic, payload)
    sock.sendto(data, (multicast_group, PORT))
    
    print(f"[PUBLISHER] Sent to [{topic}] ({multicast_group}): {payload}")
    sock.close()

if __name__ == "__main__":
    print("--- Starting Multicast Publisher ---")
    publish("NEWS", "Breaking News: Python 3.15 released!")
    time.sleep(1)
    publish("TECH", "New AI model announced today.")
    time.sleep(1)
    publish("SPORTS", "Local team wins the championship!")
    print("--- Done ---")