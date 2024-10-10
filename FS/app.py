from flask import Flask, request
import socket
import json

app = Flask(__name__)

def register_with_as(hostname, ip, as_ip, as_port):
    message = f"TYPE-A\nNAME-{hostname}\nVALUE-{ip}\nTTL-10\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (as_ip, int(as_port)))

@app.route("/register", methods=['PUT'])
def register():
    data = request.json
    register_with_as(data['hostname'], data['ip'], data['as_ip'], data['as_port'])
    return "Registered with AS", 201

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

@app.route("/fibonacci")
def fibonacci_route():
    number = request.args.get('number')
    try:
        number = int(number)
        return str(fibonacci(number)), 200
    except (TypeError, ValueError):
        return "Bad Request", 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090)
