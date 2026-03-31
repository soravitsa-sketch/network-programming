# utils/protocol.py
import json
import uuid

def create_message(sender_id, msg_type, content, msg_id=None):
    """สร้างแพ็กเกจข้อความในรูปแบบ JSON"""
    return json.dumps({
        "msg_id": msg_id or str(uuid.uuid4()),
        "sender_id": sender_id,
        "type": msg_type,
        "content": content
    })

def parse_message(data):
    """แปลงข้อมูล JSON กลับเป็น Dictionary"""
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return None