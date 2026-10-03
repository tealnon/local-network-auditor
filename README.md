# Local Network Reconnaissance Suite

A modular Python tool suite built for local network auditing, asset discovery, and endpoint intelligence gathering. Designed to emphasize low-level frame transmission and rapid service enumeration.

## 🛠️ Tech Stack & Skills

* **Language:** Python 3
* **Libraries:** `scapy`, `socket`, `concurrent.futures`
* **Core Concepts:** Layer 2 packet crafting, TCP handshaking, concurrent socket polling, and json parsing
* **Domain:** Offensive Security & Recon

## 🔑 Key Features

### 🚀 Features
* **Layer 2 ARP Discovery:** Broadcasts custom ARP requests to map live targets on isolated network segments.
* **Hardware Fingerprinting:** Resolves MAC addresses against vendor databases to profile connected infrastructure.
* **Concurrent TCP Sweeping:** Executes multi-threaded port checks to minimize enumeration time.
* **Endpoint Probing:** Queries local device endpoints (`/setup/eureka_info`, etc.) for configuration intelligence.

## ⚡ Quickstart & Setup

### 1. Prerequisites
* Python 3.8+ installed
* Elevated permissions for raw network interface binding

### 2. Installation
Clone the repository and prepare your environment:

```bash
git clone https://github.com/tealnon/local-network-auditor
cd local-network-auditor

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1 # Windows
# source venv/bin/activate # Linux/Mac

# Install dependencies
pip install scapy