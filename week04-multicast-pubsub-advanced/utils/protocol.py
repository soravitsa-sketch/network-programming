# utils/protocol.py
import json
import time

def encode_message(topic, payload):
    """แปลงข้อมูลให้อยู่ในรูป JSON และเข้ารหัสเป็น Byte"""
    msg = {
        "topic": topic,
        "payload": payload,
        "timestamp": time.time()
    }
    return json.dumps(msg).encode('utf-8')

def decode_message(data):
    """ถอดรหัส Byte กลับมาเป็น Dictionary (JSON)"""
    return json.loads(data.decode('utf-8'))