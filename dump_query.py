import json
import urllib.request

target_ip = "192.168.1.89"
url = f"http://{target_ip}:8008/setup/eureka_info"

print(f"[*] Querying local API on {target_ip}...")

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=3) as response:
        data = json.loads(response.read().decode())
        
        # Print the entire raw JSON payload to see all available keys
        print("\n[+] Full Raw Device JSON:")
        print(json.dumps(data, indent=2))

except Exception as e:
    print(f"[-] Failed to query device API: {e}")