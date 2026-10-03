import socket
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from scapy.all import ARP, Ether, srp

socket.setdefaulttimeout(1.0)

def get_mac_vendor(mac: str) -> str:
    """Looks up the manufacturer of a MAC address via API."""
    try:
        url = f"https://api.maclookup.app/v2/macs/{mac}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
            company = data.get("company", "")
            return company if company else "Unknown Vendor"
    except Exception:
        return "Unknown Vendor"

def resolve_hostname(ip: str) -> str:
    """Attempts reverse DNS lookup to get the device's network name."""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except (socket.herror, socket.timeout, OSError):
        return "-"

def scan_port(ip: str, port: int):
    """Checks if a specific TCP port is open on a target IP."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.4)
        if s.connect_ex((ip, port)) == 0:
            print(f" [+] Port {port} is OPEN")
        s.close()
    except Exception:
        pass

def audit_target(host_info: dict, ports: list):
    """Runs a multithreaded port scan against a single discovered host."""
    ip = host_info["ip"]
    print(f"\n[*] Scanning ports for {ip} ({host_info['vendor']})...")
    with ThreadPoolExecutor(max_workers=20) as executor:
        for port in ports:
            executor.submit(scan_port, ip, port)

def network_auditor(ip_range: str):
    print(f"[*] Starting network audit on subnet: {ip_range}...\n")

    # Step 1: ARP Sweep
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req = ARP(pdst=ip_range)
    packet = broadcast / arp_req

    answered_list = srp(packet, timeout=2, verbose=False)[0]

    print(f"{'IP Address':<16} {'MAC Address':<18} {'Vendor / Manufacturer':<28} {'Hostname'}")
    print("-" * 78)
    
    discovered_hosts = []
    for sent, received in answered_list:
        ip = received.psrc
        mac = received.hwsrc
        vendor = get_mac_vendor(mac)
        hostname = resolve_hostname(ip)

        host_info = {"ip": ip, "mac": mac, "vendor": vendor, "hostname": hostname}
        discovered_hosts.append(host_info)
        print(f"{ip:<16} {mac:<18} {vendor:<28} {hostname}")

    print(f"\n[*] Found {len(discovered_hosts)} active host(s).")

    # Step 2: Automated Port Sweeping on Discovered Hosts
    common_ports = [22, 80, 443, 554, 1883, 8008, 8009, 9100]
    for host in discovered_hosts:
        audit_target(host, common_ports)

    print("\n[*] Network audit complete.")

if __name__ == "__main__":
    network_auditor("192.168.1.1/24")
