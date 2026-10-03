import json
import urllib.request

target_ip = "192.168.1.89"
url = f"http://{target_ip}:8008/setup/eureka_info"

device_name = "Unknown"
model = "Unknown"
manufacturer = "Unknown"

print(f"[*] Querying local API on {target_ip}...")

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=3) as response:
        data = json.loads(response.read().decode())
        device_name = data.get("name", "Unknown")
        
        # Safely extract nested device_info keys
        dev_info = data.get("device_info", {})
        if isinstance(dev_info, dict):
            model = dev_info.get("model_name", "Unknown")
            manufacturer = dev_info.get("manufacturer", "Unknown")

except Exception as e:
    print(f"[-] Failed to query device API: {e}")

print(f"\n[+] Device Name: {device_name}")
print(f"[+] Manufacturer: {manufacturer}")
print(f"[+] Model: {model}")