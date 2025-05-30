import time
import hashlib
import socket
import json

# Configuration for the merchant's server
MERCHANT_HOST = '192.168.1.7'
MERCHANT_PORT = 8889

BANK_HOST = '192.168.1.7'
BANK_PORT = 9999

class User:
    def __init__(self, name, password, ifsc_code, balance, pin_code, phone_number):
        self.name = name
        self.password = password
        self.ifsc_code = ifsc_code
        self.balance = balance
        self.pin_code = pin_code
        self.phone_number = phone_number
        self.account_creation_time = time.time()  # Store the account creation time
        #Bank generates the following details
        self.uid = None  
        self.mmid = None

    def __repr__(self):
        return f"{self.name} - {self.ifsc_code} - {self.balance} - {self.phone_number}"
    
    def register_with_bank(self, bank_host = BANK_HOST, bank_port = BANK_PORT):
        registration_data = {
            "action": "register_user",
            "name": self.name,
            "password": self.password,
            "ifsc_code": self.ifsc_code,
            "balance": self.balance,
            "pin_code": self.pin_code,
            "phone_number": self.phone_number
        }
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((bank_host, bank_port))
                s.send(json.dumps(registration_data).encode())
                response = s.recv(4096)
                resp = json.loads(response.decode())
                if resp.get("status") == "success":
                    self.uid = resp.get("uid")
                    self.mmid = resp.get("mmid")
                    print("Registration successful!")
                else:
                    print("Registration failed:", resp.get("message"))
                return resp
        except Exception as e:
            print("Error during registration:", str(e))
            return {"status": "error", "message": str(e)}
            
    def send_transaction(self, encrypted_merchant_id, pin, amount):
        #Connects to the merchant and sends the transaction details.
        def simple_permutation_encrypt(data):
                # Simple permutation encryption: reverse the string representation of the data
                json_data = json.dumps(data)  # Convert data to JSON string
                encrypted_data = json_data[::-1]  # Reverse the string
                return encrypted_data
        
        print("Sending transaction request to merchant at", MERCHANT_HOST, MERCHANT_PORT)
        transaction_data = {
            "encrypted_merchant_id": encrypted_merchant_id,
            "mmid": self.mmid,
            "pin": pin,
            "amount": amount
        }

        transaction_data = simple_permutation_encrypt(transaction_data)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((MERCHANT_HOST, MERCHANT_PORT))
                client.send(transaction_data.encode())
                response = client.recv(4096)
                return json.loads(response.decode())
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
def main():
    print("User Registration and Transaction System")
    name = input("Enter your name: ").strip()
    password = input("Enter your password: ").strip()
    ifsc_code = input("Enter your IFSC code: ").strip()
    balance = float(input("Enter your initial balance: ").strip())
    pin_code = input("Enter your PIN code: ").strip()
    phone_number = input("Enter your phone number: ").strip()

    #create a user
    user = User(name, password, ifsc_code, balance, pin_code, phone_number)

    # Register the user with the bank
    print("Registering user with the bank...")
    registration_response = user.register_with_bank()
    if registration_response.get("status") == "success":
        print(f"User registered successfully with MMID: {user.mmid} and UID: {user.uid}")
    else:
        print("Registration failed:", registration_response.get("message"))

    # Send a transaction
    while True:
        encrypted_merchant_id = input("Enter the encrypted merchant ID: ").strip()
        amount = int(input("Enter the transaction amount: ").strip())
        pin = input("Enter your PIN: ").strip()
        transaction_response = user.send_transaction(encrypted_merchant_id, pin, amount)
        print("Transaction Response:", transaction_response)

if __name__ == "__main__":
    main()