**The project is prepared by the following members:**

**1\. Deepal Deep (Team Leader)**

**2\. Kumar Animesh**

**Secure Payment System over Intranet using QR and Blockchain**

**Overview of the Project:**

This project simulates a **secure digital payment system** involving three key entities: **User**, **Merchant**, and **Bank**—all communicating over sockets. The system emulates real-time transactions, account management, and a blockchain-based ledger for transparency.

* **User**: Can register with the bank, receive a unique MMID/UID, and initiate payments using a secure PIN and encrypted merchant ID.

* **Merchant**: Registers with the bank to get a unique Merchant ID, encrypts it using a simple permutation cipher to generate a VMID, and displays it as a QR code for customers.

* **Bank**: Handles user and merchant registrations, transaction validation, balance updates, and maintains an immutable blockchain ledger of all transactions.

Each component runs on a different IP and port. Communication is via JSON over TCP sockets. Transactions are recorded with timestamped blocks, ensuring traceability and tamper-resistance.

The system uses **simple encryption** for demonstration purposes and is designed for educational use—ideal for understanding core concepts of fintech architecture, encryption, and blockchain logging

***This project simulates a digital payment system with three core components:***

***\- Bank Server (\`bank.py\`)***

***\- Merchant Server (\`merchant.py\`)***

***\- User Client (\`user.py\`)***

***\- Blockchain Viewer (\`fetch\_blocks.py\`)***

Transactions are processed securely using QR code-based identification, encrypted data exchange, and a custom blockchain ledger for verification and recordkeeping.

Prerequisites

\- Python 3.9+

\- Dependencies (install using pip):

**Steps:**

pip install cryptography qrcode pillow

**File Overview**

* bank.py – Runs the central bank server, handles registrations, and maintains the blockchain.

* merchant.py – Registers the merchant with the bank, generates an encrypted VMID, and handles transactions.

* user.py – Allows users to register and transact with merchants using the MMID and PIN.

* fetch\_blocks.py – Fetches and displays the blockchain from the bank server.

**How to Run**

1\. Start the Bank Server

**Run this in one terminal. The bank should be started first.**

**python bank.py**

2\. Start the Merchant Server

**Open a second terminal and run:**

**python merchant.py**

You will be prompted to enter merchant name, ID, and PIN. Upon registration, the merchant server will generate and display a QR code representing the encrypted VMID.

3\. Run the User Client

**Open a third terminal and run:**

**python user.py**

Register a new user (name, ID, PIN), then scan a merchant’s QR code and perform a transaction by entering amount and your PIN.

4\. View the Blockchain

You can verify if a transaction was added successfully using:

**python fetch\_blocks.py**

This retrieves and prints the current blockchain from the bank server.

**Shor's Algorithm RSA Attack Demonstration**

This Python script demonstrates how Shor's algorithm (designed for quantum computers) can be used to break RSA encryption by efficiently factoring large numbers.

This is a simplified simulation of how Shor's algorithm works, created as part of a Cryptography assignment. The script demonstrates:

1. RSA key generation (using small keys for demonstration)  
2. Encryption of a message using RSA  
3. A simulation of Shor's algorithm factoring the RSA modulus  
4. Recovery of the private key and decryption of the message

Requirements

* Python 3.6+  
* NumPy  
* SymPy

Installation

Install the required dependencies:

**pip install numpy sympy**

Run the script with:

**python shors\_algorithm\_demo.py**

The script demonstrates the following steps:

1. **RSA Encryption**:  
   * Generates small RSA keys (10-bit primes for demonstration)  
   * Encrypts a sample message "QUANTUM"  
   * Verifies encryption by decrypting with the private key  
2. **Shor's Algorithm Simulation**:  
   * Simulates the period-finding function of Shor's algorithm  
   * Uses the period to factor the RSA modulus into its prime components  
   * Note: In a real quantum computer, this would be done using quantum operations  
3. **Attack Demonstration**:  
   * Uses the factorization to recover the private key  
   * Decrypts the message with the recovered key

