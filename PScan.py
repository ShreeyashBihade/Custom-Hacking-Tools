import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

open_ports = []

def scan_tcp(host, port, timeout, grab_banner):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            if result == 0:
                banner = ""
                if grab_banner:
                    try:
                        sock.sendall(b"HEAD / HTTP/1.1\r\nHost: {}\r\n\r\n".format(host).encode())
                        banner = sock.recv(1024).decode(errors="ignore").strip()
                    except:
                        banner = "No banner"
                return (port, "TCP", banner)
    except:
        pass
    return None

def scan_udp(host, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(timeout)
            sock.sendto(b'', (host, port))
            sock.recvfrom(1024)
    except socket.timeout:
        return (port, "UDP", "Open|Filtered")  # no reply, might be open
    except socket.error:
        return None
    return (port, "UDP", "Open (received response)")

def main():
    parser = argparse.ArgumentParser(description="🚀 Fast Full-Port Scanner (TCP/UDP)")
    parser.add_argument("-H", "--host", required=True, help="Target IP or domain")
    parser.add_argument("-t", "--timeout", type=float, default=0.5, help="Timeout per port in seconds (default: 0.5)")
    parser.add_argument("-T", "--threads", type=int, default=500, help="Number of threads (default: 500)")
    parser.add_argument("-b", "--banner", action="store_true", help="Enable banner grabbing (TCP only)")
    parser.add_argument("-u", "--udp", action="store_true", help="Enable UDP scan")
    args = parser.parse_args()

    print(f"\n🔎 Scanning {args.host} (1-65535) | UDP: {args.udp} | Threads: {args.threads} | Timeout: {args.timeout}\n")

    ports = range(1, 65535)
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        scan_func = scan_udp if args.udp else lambda port: scan_tcp(args.host, port, args.timeout, args.banner)
        futures = {executor.submit(scan_func, port): port for port in ports}

        for future in tqdm(as_completed(futures), total=len(futures), desc="Scanning"):
            result = future.result()
            if result:
                port, proto, banner = result
                open_ports.append((port, proto))
                print(f"[+] {proto} Port {port} is OPEN", end='')
                if args.banner and proto == "TCP":
                    print(f" | Banner: {banner}")
                else:
                    print()

    print("\n✅ Scan complete.")
    if open_ports:
        print("Open ports:")
        for port, proto in open_ports:
            print(f"  {proto} {port}")
    else:
        print("No open ports found.")

if __name__ == "__main__":
    main()
