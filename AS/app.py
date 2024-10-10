from socket import socket, AF_INET, SOCK_DGRAM
import json

records = {}

def handle_query(data, addr, sock):
    lines = data.strip().split('\n')
    if "TYPE-A" in data:
        nkey = lines[1].split('-')[1]
        ipaddr = lines[2].split('-')[1]
        records[nkey] = ipaddr
        sock.sendto(b"Registered", addr)
    else:
        key = data.split('=')[1].strip()
        if key in records:
            response = f"TYPE=A\nNAME-{key}\nVALUE-{records[key]}\nTTL=10\n"
            sock.sendto(response.encode(), addr)
        else:
            sock.sendto(b"Not found", addr)

def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('', 53533))
    while True:
        data, addr = sock.recvfrom(1024)
        handle_query(data.decode(), addr, sock)

if __name__ == "__main__":
    main()