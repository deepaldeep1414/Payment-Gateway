# fetch_blocks.py

import socket, json

BANK_HOST = '192.168.1.7'
BANK_PORT = 9999

def fetch_blockchain():
    req = {"action": "get_blockchain"}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((BANK_HOST, BANK_PORT))
        s.send(json.dumps(req).encode())
        response = json.loads(s.recv(65536).decode())
        return response

response = fetch_blockchain()
if response['status'] == 'success':
    for i, block in enumerate(response['chain']):
        print(f"\n--- Block {i} ---")
        for key, value in block.items():
            print(f"{key}: {value}")
else:
    print("Error:", response.get("message"))
