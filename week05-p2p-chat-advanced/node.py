# node.py
import socket
import threading
import sys
import time
from config import HOST, BASE_PORT, BROADCAST_PORT, BUFFER_SIZE
from peer_table import PeerTable
from router import Router
from utils.protocol import create_message, parse_message

class P2PNode:
    def __init__(self, node_id):
        self.node_id = str(node_id)
        self.port = BASE_PORT + int(node_id)
        self.peer_table = PeerTable()
        self.router = Router()
        self.running = True

    def start(self):
        # 1. เริ่ม Thread สำหรับฟัง TCP (รับข้อความแชท)
        threading.Thread(target=self.tcp_listener, daemon=True).start()
        
        # 2. เริ่ม Thread สำหรับฟัง UDP (Discovery)
        threading.Thread(target=self.udp_discovery_listener, daemon=True).start()
        
        # 3. เริ่ม Thread สำหรับส่ง UDP Broadcast ประกาศตัว
        threading.Thread(target=self.udp_broadcaster, daemon=True).start()

        print(f"=== เริ่มต้น Node {self.node_id} บนพอร์ต {self.port} ===")
        print("พิมพ์ข้อความแล้วกด Enter เพื่อส่งหาทุกคน (Flooding) หรือพิมพ์ 'exit' เพื่อออก\n")

        # Main Loop: รับข้อความจากผู้ใช้
        try:
            while self.running:
                msg_content = input()
                if msg_content.lower() == 'exit':
                    self.shutdown()
                    break
                if msg_content:
                    self.send_chat_message(msg_content)
        except KeyboardInterrupt:
            self.shutdown()

    def tcp_listener(self):
        """ฟังข้อความแชทแบบ TCP ที่เข้ามา"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, self.port))
        server.listen(5)
        
        while self.running:
            try:
                conn, addr = server.accept()
                data = conn.recv(BUFFER_SIZE).decode()
                msg = parse_message(data)
                
                if msg and msg["type"] == "CHAT":
                    # ถ้าระบุว่าเป็นข้อความใหม่ ให้พิมพ์ออกมา และส่งต่อ (Flooding)
                    if self.router.is_new_message(msg["msg_id"]):
                        print(f"\n[{msg['sender_id']}]: {msg['content']}")
                        self.flood_message(data, exclude_port=addr[1])
                        
                conn.close()
            except:
                pass

    def udp_discovery_listener(self):
        """ฟังการประกาศตัวจาก Node อื่นๆ ทาง UDP"""
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # อนุญาตให้ใช้พอร์ต Broadcast ร่วมกัน (เพื่อจำลองรันหลาย Node ในเครื่องเดียว)
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_sock.bind(('', BROADCAST_PORT))

        while self.running:
            try:
                data, addr = udp_sock.recvfrom(BUFFER_SIZE)
                msg = parse_message(data.decode())
                
                if msg and msg["type"] == "DISCOVERY" and msg["sender_id"] != self.node_id:
                    peer_port = msg["content"]["port"]
                    self.peer_table.add_peer(addr[0], peer_port)
            except:
                pass

    def udp_broadcaster(self):
        """ส่งข้อความทักทาย (Heartbeat) เพื่อบอกเพื่อนๆ ว่าฉันอยู่ที่นี่"""
        udp_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_out.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        while self.running:
            msg = create_message(self.node_id, "DISCOVERY", {"port": self.port})
            try:
                # ส่งไปยังที่อยู่ Broadcast ของเครือข่าย (ในกรณีทดสอบเครื่องเดียวใช้ <broadcast>)
                udp_out.sendto(msg.encode(), ('<broadcast>', BROADCAST_PORT))
            except:
                pass
            time.sleep(3) # ประกาศตัวทุกๆ 3 วินาที

    def send_chat_message(self, content):
        """สร้างข้อความใหม่และเริ่มกระบวนการ Flooding"""
        msg = create_message(self.node_id, "CHAT", content)
        msg_dict = parse_message(msg)
        self.router.is_new_message(msg_dict["msg_id"]) # บันทึกว่าเราเป็นคนส่งเอง จะได้ไม่รับซ้ำ
        self.flood_message(msg)

    def flood_message(self, raw_message, exclude_port=None):
        """ส่งข้อความไปยัง Peer ทุกคนที่รู้จัก (Gossip/Flooding)"""
        for ip, port in self.peer_table.get_peers():
            if port == exclude_port:
                continue # ไม่ส่งกลับไปหาคนที่เพิ่งส่งมาให้เรา
            
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect((ip, port))
                sock.sendall(raw_message.encode())
                sock.close()
            except:
                # ถ้าส่งไม่ได้ แสดงว่า Peer อาจจะปิดไปแล้ว ให้ลบออกจากตาราง
                self.peer_table.remove_peer(ip, port)

    def shutdown(self):
        """ปิดการทำงานอย่างปลอดภัย (Graceful Shutdown)"""
        print("\n[SYSTEM] กำลังปิดระบบ...")
        self.running = False
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("วิธีใช้งาน: python node.py <node_id>")
        sys.exit(1)
    
    node = P2PNode(sys.argv[1])
    node.start()