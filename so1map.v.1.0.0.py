import socket
import sys
from datetime import datetime

print("jmap")
target_ip = str(input("Enter a ip: "))
print("_" * 50)
print(f"[!] Scanning Target {target_ip}")
print(f"[!] Scanning started at: {datetime.now()}")
print("_" * 50)

try:

    for port in range(1,65535):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)

        result = s.connect_ex((target_ip, port))
        if result == 0:
            print(f"[*] port {port} is open")
        s.close()
except KeyboardInterrupt:
    print(f"[!] CTRL + C DETECTED EXITING...")
    sys.exit()

except socket.error:
    print(f"[!] host not responding :(")
    sys.exit()
