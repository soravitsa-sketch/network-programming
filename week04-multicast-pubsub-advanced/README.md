# Advanced Multicast Publish/Subscribe System

A robust, topic-based Publish/Subscribe (Pub/Sub) messaging system built natively in Python using UDP IP Multicast. 

This project demonstrates how to leverage network-level multicast routing to achieve efficient, scalable message distribution without the need for a centralized message broker (like RabbitMQ or Kafka).

---

## 🏗️ System Architecture

The system utilizes the **Internet Group Management Protocol (IGMP)** concept via UDP sockets. Instead of sending messages to individual clients (Unicast) or flooding the network (Broadcast), it maps logical application "Topics" to specific Class D Multicast IP Addresses (Range: `224.0.0.0` - `239.255.255.255`).

* **Publisher:** Encodes messages into JSON format and transmits them via UDP to a specific Multicast IP representing a topic.
* **Subscriber:** Binds to a local port and explicitly joins a Multicast Group (`socket.IP_ADD_MEMBERSHIP`) to selectively listen only to topics of interest.
* **Protocol:** Messages are encapsulated in JSON payloads, allowing for extensible metadata (e.g., timestamps, headers) alongside the main content.

---

## ✨ Key Features

* **Network-Level Topic Isolation:** Subscribers inherently filter out unwanted messages at the network layer, preventing unnecessary CPU processing.
* **Decentralized:** No central server or broker is required to route messages.
* **Zero-Configuration Discovery:** Subscribers and Publishers can join and leave the network dynamically without notifying each other.
* **JSON Serialization:** Standardized data exchange format using a custom `utils.protocol` module.

---

## 📂 Repository Structure

```text
week04-multicast-pubsub-advanced/
├── config.py           # Global network configurations (PORT, BUFFER_SIZE, TTL)
├── topics.py           # Mapping dictionary for Topics to Multicast IP addresses
├── publisher.py        # Broadcasts messages to specific topics
├── subscriber.py       # Joins multicast groups and listens for incoming data
├── utils/
│   └── protocol.py     # JSON serialization and deserialization helpers
└── README.md           # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
* Python 3.8 or higher
* No external dependencies required (uses Python Standard Library: `socket`, `struct`, `json`)

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/week04-multicast-pubsub-advanced.git](https://github.com/yourusername/week04-multicast-pubsub-advanced.git)
   cd week04-multicast-pubsub-advanced
   ```

### Usage Instructions

To fully observe the Multicast behavior, you will need to open multiple terminal windows.

**Step 1: Start the Subscribers**
Open two separate terminals and subscribe to different topics. The system currently supports `NEWS`, `SPORTS`, and `TECH`.

*Terminal 1 (Listening to NEWS):*
```bash
python subscriber.py NEWS
```

*Terminal 2 (Listening to TECH):*
```bash
python subscriber.py TECH
```

**Step 2: Run the Publisher**
Open a third terminal and execute the publisher script. The publisher will iterate through predefined messages and send them to their respective topics.

*Terminal 3:*
```bash
python publisher.py
```

**Step 3: Observe the Results**
You will notice that *Terminal 1* only prints messages related to `NEWS`, and *Terminal 2* only prints messages related to `TECH`. Any messages sent to `SPORTS` are dropped by the network interface, demonstrating true selective listening.

---

## 🧠 Design Decisions & Networking Concepts

* **`SO_REUSEADDR`:** Implemented in `subscriber.py` to allow multiple subscribers running on the same physical machine to bind to the same UDP port successfully.
* **TTL (Time-To-Live):** Set to `1` in `config.py` to restrict multicast packets to the local subnet, preventing accidental routing over the public internet.
* **`struct.pack("4sl", ...)`:** Used to construct the IGMP join request at the byte level, which is required by the OS kernel to update the network interface's multicast routing table.