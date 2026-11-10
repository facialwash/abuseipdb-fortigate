
import os
import ipaddress
import urllib.request
import urllib.parse
from pathlib import Path

API_KEY = os.environ.get("ABUSEIPDB_API_KEY")

if not API_KEY:
    raise RuntimeError("ABUSEIPDB_API_KEY is missing")

API_URL = "https://api.abuseipdb.com/api/v2/blacklist"

params = {
    "confidenceMinimum": "90",
    "limit": "10000",
    "ipVersion": "4"
}

url = API_URL + "?" + urllib.parse.urlencode(params)

headers = {
    "Key": API_KEY,
    "Accept": "text/plain"
}

request = urllib.request.Request(url, headers=headers)

with urllib.request.urlopen(request, timeout=60) as response:
    if response.status != 200:
        raise RuntimeError(f"API error: {response.status}")

    content = response.read().decode("utf-8")

# Validate and normalize IPv4 addresses
ips = set()

for line in content.splitlines():
    line = line.strip()

    if not line:
        continue

    ip = ipaddress.ip_address(line)

    if ip.version == 4:
        ips.add(str(ip))

if not ips:
    raise RuntimeError("Blacklist is empty. Existing file preserved.")

sorted_ips = sorted(
    ips,
    key=lambda x: int(ipaddress.ip_address(x))
)

output = Path("blacklist.txt")
output.write_text("\n".join(sorted_ips) + "\n", encoding="utf-8")

print(f"Successfully retrieved {len(sorted_ips)} IPv4 addresses")
print("Blacklist updated successfully")
