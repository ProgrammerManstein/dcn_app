from flask import Flask, request
import requests
import socket

app = Flask(__name__)

def query_dns(hostname, as_ip, as_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = f"TYPE=ANAME={hostname}"
    sock.sendto(message.encode(), (as_ip, int(as_port)))
    response, _ = sock.recvfrom(1024)
    return response.decode().split('VALUE-')[1].split(' ')[0]

@app.route("/fibonacci")
def fibonacci():
    args = request.args
    hostname = args.get('hostname')
    fs_port = args.get('fs_port')
    number = args.get('number')
    as_ip = args.get('as_ip')
    as_port = args.get('as_port')
    if None in [hostname, fs_port, number, as_ip, as_port]:
        return "Bad Request", 400
    fs_ip = query_dns(hostname, as_ip, as_port)
    response = requests.get(f"http://{fs_ip}:{fs_port}/fibonacci?number={number}")
    return response.text, response.status_code

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
