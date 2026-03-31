# Week 5 – Advanced Lab: Decentralized Chat Overlay

A peer-to-peer (P2P) chat network built with Python's `socket` and `threading` modules. Every node acts as both a client and a server, communicating without any central authority.

## Features

| Feature | Details |
|---|---|
| **Dynamic Peer Discovery** | Nodes find each other automatically using UDP Local Broadcast |
| **Gossip / Flooding Protocol** | Chat messages are forwarded (flooded) to all known peers |
| **Loop Prevention** | Message UUIDs are tracked to prevent infinite broadcast storms |
| **Symmetric Roles** | Each node listens for connections while simultaneously sending data |
| **Graceful Shutdown** | Disconnected nodes are automatically removed from routing tables |

---

## Directory Structure

```text
week05-p2p-chat-advanced/
├── config.py               # Shared HOST / PORTs / Buffer limits
├── node.py                 # Entry point; main P2P Node logic
├── peer_table.py           # Manages the list of known peers
├── router.py               # Tracks Message IDs for loop prevention
└── utils/
    ├── __init__.py         
    └── protocol.py         # JSON message formatting & UUID generation
```

---

## How to Run

> All commands must be run from the **project root** (`week05-p2p-chat-advanced/`).

### 1 — Start the first Node

```bash
python node.py 1
```

Expected output:
```text
=== เริ่มต้น Node 1 บนพอร์ต 9001 ===
พิมพ์ข้อความแล้วกด Enter เพื่อส่งหาทุกคน (Flooding) หรือพิมพ์ 'exit' เพื่อออก
```

### 2 — Connect more Nodes (open a new terminal per node)

```bash
python node.py 2
```
```bash
python node.py 3
```

Open **two or more** terminals and use a different Node ID (1, 2, 3...) for each. Within a few seconds, nodes will discover each other:
```text
[SYSTEM] ค้นพบ Peer ใหม่: 127.0.0.1:9001
[SYSTEM] ค้นพบ Peer ใหม่: 127.0.0.1:9002
```

### 3 — Chat

- Type any message in any terminal and press **Enter** to send.
- The message will be flooded to all other connected nodes.
- Type `exit` to disconnect cleanly.

### 4 — Stop the Node

Type `exit` and press Enter, or press **Ctrl+C** in the terminal.

---

## Configuration (`config.py`)

| Variable | Default | Purpose |
|---|---|---|
| `HOST` | `127.0.0.1` | Loopback address |
| `BASE_PORT` | `9000` | Base TCP port (Node ID gets added to this) |
| `BROADCAST_PORT` | `9999` | UDP port used for peer discovery |
| `BUFFER_SIZE` | `2048` | Recv buffer in bytes |

---

## Architecture

```text
Node A (Client + Server)
│
├── UDP Broadcaster ──► (Discovers Node B & C via port 9999)
├── UDP Listener    ◄── (Receives discovery from B & C)
│
├── TCP Listener    ◄── (Receives chat from B & C)
│
PeerTable & Router (Shared state)
│
└── Sender/Flooder  ──► (Forwards new chat messages to B & C)
```

---

## Common Issues

| Symptom | Cause | Fix |
|---|---|---|
| `Address already in use` | Node ID reused or port taken | Use a unique Node ID for each terminal (e.g., 1, 2, 3) |
| No discovery messages | UDP Broadcast blocked | Ensure OS Firewall allows UDP traffic on port `9999` |
| Messages echoing back | Router not tracking IDs | Ensure `protocol.py` is generating unique `msg_id` |

---

## Extension Ideas

- **Persistent Peer List** — Save known peers to a `.json` file to remember them across restarts.
- **Direct Messaging** — Add routing logic for `/pm <node_id> <message>`.
- **File Transfer** — Support sending files over dedicated TCP streams instead of just JSON text.