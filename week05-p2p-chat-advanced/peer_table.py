# peer_table.py
class PeerTable:
    def __init__(self):
        # เก็บข้อมูล peer ในรูปแบบ set ของ tuple (ip, port) เพื่อป้องกันข้อมูลซ้ำ
        self.peers = set()

    def add_peer(self, ip, port):
        peer = (ip, int(port))
        if peer not in self.peers:
            self.peers.add(peer)
            print(f"\n[SYSTEM] ค้นพบ Peer ใหม่: {ip}:{port}")

    def get_peers(self):
        return list(self.peers)

    def remove_peer(self, ip, port):
        peer = (ip, int(port))
        if peer in self.peers:
            self.peers.discard(peer)
            print(f"\n[SYSTEM] ลบ Peer ออกจากการเชื่อมต่อ: {ip}:{port}")