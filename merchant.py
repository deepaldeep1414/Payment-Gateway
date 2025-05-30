import socket
import json
from cryptography.fernet import Fernet
import qrcode


# Configuration
MERCHANT_HOST = '172.20.50.12'
MERCHANT_PORT = 8889

BANK_HOST = '192.168.1.7'
BANK_PORT = 9999

class Merchant:
    def __init__(self, name, password, ifsc_code, balance):
        self.name = name
        self.password = password
        self.ifsc_code = ifsc_code
        self.balance = balance
        self.merchant_id = None
        self.key = 5

    def register_with_bank(self):
        request = {
            "action": "register_merchant",
            "name": self.name,
            "password": self.password,
            "ifsc_code": self.ifsc_code,
            "balance": self.balance
        }

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bank_socket:
                bank_socket.connect((BANK_HOST, BANK_PORT))
                bank_socket.send(json.dumps(request).encode())
                response = json.loads(bank_socket.recv(4096).decode())

                if response['status'] == 'success':
                    self.merchant_id = response['merchant_id']
                    print(f"[MERCHANT] Registered with Bank | Merchant ID: {self.merchant_id}")
                else:
                    print("[MERCHANT] Registration failed:", response['message'])

        except Exception as e:
            print("[MERCHANT] Error registering with bank:", str(e))
        
        # Encrypt the merchant ID to create a VMID
        try:
            # Simple permutation encryption function
            def simple_permutation_encrypt(key, plaintext):
                return ''.join(chr((ord(char) + key) % 256) for char in plaintext)

            # Encrypt the merchant ID using simple permutation encryption
            vmid = simple_permutation_encrypt(self.key, self.merchant_id)
            print(f"[MERCHANT] VMID (Encrypted Merchant ID): {vmid}")

            # Generate a QR code for the VMID
            qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
            qr.add_data(vmid)
            qr.make(fit=True)

            # Display the QR code
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_image.show()
            print("[MERCHANT] QR Code displayed.")

        except Exception as e:
            print("[MERCHANT] Error generating VMID or QR Code:", str(e))

    def handle_user_transaction(self, client_socket):
        def simple_permutation_decipher_json(self, encrypted_data):
            # Simple permutation decryption: reverse the string back to original
            decrypted_data = encrypted_data[::-1]  # Reverse the string
            return json.loads(decrypted_data)  # Convert back to dictionary
        
        try:
            data = client_socket.recv(4096)
            transaction_request = simple_permutation_decipher_json(self, data.decode())
            # transaction_request = json.loads(data.decode())
            print("[MERCHANT] Received transaction request:", transaction_request)
            # Decrypt the encrypted merchant ID (VMID) to retrieve the original merchant ID
            try:
                # Simple permutation decryption function
                def simple_permutation_decrypt(key, ciphertext):
                    return ''.join(chr((ord(char) - key) % 256) for char in ciphertext)

                # Decrypt the encrypted merchant ID (VMID) using simple permutation decryption
                decrypted_merchant_id = simple_permutation_decrypt(self.key, transaction_request['encrypted_merchant_id'])
                print("[MERCHANT] Decrypted Merchant ID:", decrypted_merchant_id)
            except Exception as e:
                error_response = {"status": "error", "message": f"Decryption failed: {str(e)}"}
                client_socket.send(json.dumps(error_response).encode())
                return
            validation_request = {
                "action": "validate_transaction",
                "encrypted_merchant_id": decrypted_merchant_id,
                "mmid": transaction_request['mmid'],
                "pin": transaction_request['pin'],
                "amount": transaction_request['amount']
            }
            def simple_permutation_encrypt_json(data):
                # Simple permutation encryption: reverse the string representation of the data
                json_data = json.dumps(data)  # Convert data to JSON string
                encrypted_data = json_data[::-1]  # Reverse the string
                return encrypted_data
            
            # validation_request = simple_permutation_encrypt_json(validation_request)
            # Send validation request to bank
            print("[MERCHANT] Sending transaction validation request to bank...")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bank_socket:
                bank_socket.connect((BANK_HOST, BANK_PORT))
                bank_socket.send(json.dumps(validation_request).encode())
                bank_response = json.loads(bank_socket.recv(4096).decode())

            # Send bank response back to user
            client_socket.send(json.dumps(bank_response).encode())

            # Display to merchant console
            print("[MERCHANT] Transaction status:", bank_response['status'])
            print("[MERCHANT] Message:", bank_response['message'])

        except Exception as e:
            error_response = {"status": "error", "message": str(e)}
            client_socket.send(json.dumps(error_response).encode())

    def start_server(self):
        print(f"[MERCHANT] Starting merchant server on {MERCHANT_HOST}:{MERCHANT_PORT}...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((MERCHANT_HOST, MERCHANT_PORT))
            server_socket.listen()
            print("[MERCHANT] Waiting for user transactions...")

            while True:
                client_socket, addr = server_socket.accept()
                print(f"[MERCHANT] Received transaction request from {addr}")
                self.handle_user_transaction(client_socket)
                client_socket.close()


# ---------- Main ----------

def main():
    print("Merchant Registration and Transaction System")
    name = input("Enter Merchant Name: ")
    password = input("Enter Merchant Password: ")
    ifsc_code = input("Enter IFSC Code: ")
    balance = float(input("Enter Initial Balance: "))

    merchant = Merchant(name, password, ifsc_code, balance)
    merchant.register_with_bank()
    
    if merchant.merchant_id:
        merchant.start_server()
    else:
        print("[MERCHANT] Cannot start server without successful registration.")

if __name__ == "__main__":
    main()
