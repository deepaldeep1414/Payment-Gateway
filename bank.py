import socket
import json
import hashlib
import time

# Configuration
BANK_HOST = '192.168.1.7'
BANK_PORT = 9999

# In-memory databases
user_database = {}
merchant_database = {}
blockchain = []


def add_block(tx_id, mmid, merchant_id, amount, timestamp):
    prev_hash = blockchain[-1]['hash'] if blockchain else '0'*64
    block_content = f"{tx_id}{prev_hash}{timestamp}"
    block_hash = hashlib.sha256(block_content.encode()).hexdigest()
    blockchain.append({
        "tx_id": tx_id,
        "mmid": mmid,
        "merchant_id": merchant_id,
        "amount": amount,
        "timestamp": timestamp,
        "prev_hash": prev_hash,
        "hash": block_hash
    })
    print(f"[BANK][BLOCKCHAIN] Block added: {tx_id}")


# ---------- Utility Functions ----------

def create_uid(name, password, timestamp):
    raw = f"{name}{timestamp}{password}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def create_mmid(phone_number, uid):
    raw = f"{phone_number}{uid}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def generate_merchant_id(name, password, timestamp):
    raw = f"{name}{timestamp}{password}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

# ---------- User Registration ----------

def handle_user_registration(data):
    try:
        name = data['name']
        password = data['password']
        ifsc_code = data['ifsc_code']
        balance = float(data['balance'])
        pin_code = data['pin_code']
        phone_number = data['phone_number']

        timestamp = time.time()
        uid = create_uid(name, password, timestamp)
        mmid = create_mmid(phone_number, uid)

        # Store user
        user_database[mmid] = {
            "uid": uid,
            "name": name,
            "password": password,
            "ifsc_code": ifsc_code,
            "balance": balance,
            "pin_code": pin_code,
            "phone_number": phone_number,
            "timestamp": timestamp
        }

        print(f"[BANK] Registered user {name} | MMID: {mmid} | Balance: {balance}")
        return {"status": "success", "uid": uid, "mmid": mmid}

    except KeyError as e:
        return {"status": "error", "message": f"Missing field: {str(e)}"}

# ---------- Merchant Registration ----------

def handle_merchant_registration(data):
    try:
        name = data['name']
        password = data['password']
        ifsc_code = data['ifsc_code']
        balance = data['balance']

        timestamp = time.time()
        merchant_id = generate_merchant_id(name, password, timestamp)

        merchant_database[merchant_id] = {
            "name": name,
            "password": password,
            "ifsc_code": ifsc_code,
            "balance": balance, 
            "timestamp": timestamp
        }

        print(f"[BANK] Registered merchant {name} | MID: {merchant_id} | Balance: {balance}")
        return {"status": "success", "merchant_id": merchant_id}

    except KeyError as e:
        return {"status": "error", "message": f"Missing field: {str(e)}"}

# ---------- Transaction Validation ----------

def handle_transaction_validation(data):
    # def simple_permutation_decipher_json(encrypted_data):
    #         # Simple permutation decryption: reverse the string back to original
    #         decrypted_data = encrypted_data[::-1]  # Reverse the string
    #         return json.loads(decrypted_data)  # Convert back to dictionary
    # data = simple_permutation_decipher_json(data)
    try:
        mmid = data['mmid']
        pin = data['pin']
        amount = float(data['amount'])
        encrypted_merchant_id = data['encrypted_merchant_id']

        if mmid not in user_database:
            return {"status": "failure", "message": "MMID not found"}

        user = user_database[mmid]

        if pin != user['pin_code']:
            return {"status": "failure", "message": "Incorrect PIN"}

        if user['balance'] < amount:
            return {"status": "failure", "message": "Insufficient balance"}

        # Decrypt and validate merchant ID (Optional/Placeholder)
        merchant_id = encrypted_merchant_id  # Simulated decryption
        if merchant_id not in merchant_database:
            return {"status": "failure", "message": "Invalid Merchant ID"}
        merchant = merchant_database[merchant_id]

        # Deduct amount
        user['balance'] -= amount
        merchant['balance'] += amount


        timestamp = time.time()
        tx_id = hashlib.sha256(f"{mmid}{merchant_id}{timestamp}{amount}".encode()).hexdigest()
        add_block(tx_id, mmid, merchant_id, amount, timestamp)

        print(f"[BANK] Transaction of {amount} approved for {user['name']} (MMID: {mmid})")
        return {
            "status": "success",
            "message": f"Transaction of {amount} successful",
            "remaining_balance": user['balance']
        }

    except KeyError as e:
        return {"status": "error", "message": f"Missing field: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ---------- Bank Server ----------


def handle_get_blockchain():
    return {"status": "success", "chain": blockchain}


def start_bank_server():
    print(f"[BANK] Starting bank server on {BANK_HOST}:{BANK_PORT}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((BANK_HOST, BANK_PORT))
        server_socket.listen()
        print("[BANK] Waiting for user/merchant registrations and transaction validations...")

        while True:
            client_socket, addr = server_socket.accept()
            with client_socket:
                try:
                    data = client_socket.recv(4096)
                    if not data:
                        continue

                    request = json.loads(data.decode())
                    action = request.get("action")

                    if action == "register_user":
                        response = handle_user_registration(request)
                    elif action == "register_merchant":
                        response = handle_merchant_registration(request)
                    elif action == "validate_transaction":
                        response = handle_transaction_validation(request)
                    elif action == "get_blockchain":
                        response = handle_get_blockchain()
                    else:
                        response = {"status": "error", "message": "Unknown action"}

                    client_socket.send(json.dumps(response).encode())

                except Exception as e:
                    error_response = {"status": "error", "message": str(e)}
                    client_socket.send(json.dumps(error_response).encode())

if __name__ == "__main__":
    start_bank_server()