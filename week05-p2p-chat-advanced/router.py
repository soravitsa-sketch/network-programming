# router.py
class Router:
    def __init__(self):
        # เก็บ msg_id ของข้อความที่เคยได้รับแล้ว
        self.seen_messages = set()

    def is_new_message(self, msg_id):
        """ตรวจสอบว่าเป็นข้อความใหม่หรือไม่ ถ้าใหม่ให้บันทึกไว้"""
        if msg_id in self.seen_messages:
            return False
        self.seen_messages.add(msg_id)
        return True