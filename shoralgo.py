import random
import math
from fractions import Fraction
import numpy as np
import sympy  # for prime number stuff
import time  # for adding some delay to make it look like computation

# helper functions
def gcd(a, b):
    # find greatest common divisor
    while b:
        a, b = b, a % b
    return a

def mod_exp(base, exponent, mod):
    # calculate (base^exponent) % mod efficiently
    res = 1
    base = base % mod
    while exponent > 0:
        if exponent % 2 == 1:
            res = (res * base) % mod
        exponent = exponent >> 1
        base = (base * base) % mod
    return res

# Create RSA keys - using small numbers for demo!
def make_keys(bits=8):
    # generate small primes - real RSA would use way bigger numbers
    p = sympy.randprime(2**(bits-1), 2**bits)
    q = sympy.randprime(2**(bits-1), 2**bits)
    
    # make sure p and q are different
    while p == q:
        q = sympy.randprime(2**(bits-1), 2**bits)
    
    # modulus
    n = p * q
    
    # totient function - number of integers coprime to n
    phi = (p - 1) * (q - 1)
    
    # public exponent - usually 65537 in real applications
    e = 65537  
    
    # if e is too big or not coprime with phi, choose another
    if e >= phi:
        # just pick some random odd number
        e = random.randrange(3, phi, 2)
        while gcd(e, phi) != 1:
            e = random.randrange(3, phi, 2)
    
    # private exponent - modular multiplicative inverse of e
    # this is the secret key we need to find
    d = pow(e, -1, phi)
    
    return (n, e), (n, d), p, q

# encrypt a message
def encrypt(msg, pub_key):
    n, e = pub_key
    
    # convert message to numbers
    msg_nums = []
    for c in msg:
        msg_nums.append(ord(c))
    
    # encrypt each character
    cipher = []
    for m in msg_nums:
        cipher.append(mod_exp(m, e, n))
    
    return cipher

# decrypt a message
def decrypt(cipher, priv_key):
    n, d = priv_key
    
    # decrypt each number
    plain_nums = []
    for c in cipher:
        plain_nums.append(mod_exp(c, d, n))
    
    # convert back to characters
    decrypted = ""
    for m in plain_nums:
        decrypted += chr(m)
    
    return decrypted

# This is the quantum part that Shor's algorithm would do
# We're simulating it with classical computation
def find_period(a, n):
    """Find the period of a^r mod n = 1"""
    # In real Shor's algorithm, this would use quantum stuff
    # We're just brute forcing it here
    
    # if a and n aren't coprime, can't use Shor's
    if gcd(a, n) != 1:
        return None
    
    # calculate a^r mod n for increasing r until we get 1
    r = 1
    while r < 10000:  # safety limit
        if mod_exp(a, r, n) == 1:
            return r
        r += 1
    
    # couldn't find period (shouldn't happen for small numbers)
    return None

# simulate Shor's algorithm
def shor_factor(n):
    print(f"\nTrying to factor n = {n} with Shor's algorithm...")
    
    # quick check for even numbers
    if n % 2 == 0:
        print("Wait, n is even! Don't need Shor's for this.")
        return 2, n // 2
    
    # check if n is prime
    if sympy.isprime(n):
        print(f"n = {n} is prime! Nothing to factor here.")
        return n, 1
    
    # main algorithm
    attempts = 0
    max_tries = 10
    
    while attempts < max_tries:
        attempts += 1
        print(f"Attempt #{attempts}")
        
        # step 1: pick random number a < n
        a = random.randint(2, n - 1)
        
        # check if we got lucky with gcd
        if gcd(a, n) > 1:
            print(f"Got lucky! gcd({a}, {n}) = {gcd(a, n)}")
            return gcd(a, n), n // gcd(a, n)
        
        # step 2: find period using "quantum" calculation
        print(f"Running 'quantum' period finding for a = {a}...")
        time.sleep(0.5)  # fake computation delay
        r = find_period(a, n)
        
        if r is None:
            print("Period finding failed, trying another random number")
            continue
            
        print(f"Found period: r = {r}")
        
        # need even period for Shor's
        if r % 2 != 0:
            print("Period is odd! That won't work, trying again...")
            continue
        
        # step 3: calculate potential factors
        x = mod_exp(a, r // 2, n)
        
        if x == n - 1:
            print("Got a^(r/2) = -1 (mod n), trying again...")
            continue
            
        # try to find factors
        factor1 = gcd(x - 1, n)
        factor2 = gcd(x + 1, n)
        
        # check if we found a non-trivial factor
        if factor1 > 1 and factor1 < n:
            print(f"Found factor: {factor1}")
            return factor1, n // factor1
            
        if factor2 > 1 and factor2 < n:
            print(f"Found factor: {factor2}")
            return factor2, n // factor2
        
        print("Factors not found, trying again with different a")
    
    # if we get here, Shor's failed (shouldn't happen for small n)
    print("Shor's algorithm failed after max attempts!")
    print("Using a fallback method...")
    
    # use sympy as a backup
    factors = sympy.factorint(n)
    p = list(factors.keys())[0]
    return p, n // p

# recover private key from factorized n
def get_private_key(n, e, p, q):
    """Get private key d from public key and factors"""
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    return (n, d)

def main():
    print("=" * 50)
    print(" RSA ENCRYPTION & SHOR'S ALGORITHM DEMO ")
    print("=" * 50)
    
    # let's use a simple message
    message = "QUANTUM"
    print(f"Message to encrypt: {message}")
    
    # generate keys - using 10 bits for demo
    # real RSA uses 2048+ bits
    bits = 10
    pub_key, priv_key, p, q = make_keys(bits)
    n, e = pub_key
    _, d = priv_key
    
    print(f"\nGenerated RSA keys:")
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"n = {n}")
    print(f"e = {e}")
    print(f"d = {d} (this is the secret!)")
    
    # encrypt our message
    print("\nEncrypting message...")
    encrypted = encrypt(message, pub_key)
    print(f"Encrypted: {encrypted}")
    
    # decrypt to verify
    original = decrypt(encrypted, priv_key)
    print(f"Decrypted: {original}")
    
    if original != message:
        print("Something went wrong with encryption/decryption!")
        return
    
    # now the fun part - breaking RSA with Shor's algorithm
    print("\n" + "=" * 50)
    print(" ATTACK SCENARIO ")
    print("=" * 50)
    print("An attacker knows:")
    print(f"1. Public key (n={n}, e={e})")
    print(f"2. Encrypted message: {encrypted}")
    print("\nThe attacker will use Shor's algorithm to break RSA...")
    
    # simulate Shor's algorithm
    print("\nRunning Shor's algorithm...")
    time.sleep(1)  # fake computation delay
    
    p_found, q_found = shor_factor(n)
    
    print(f"\nResult of factorization:")
    print(f"Found factors: {p_found} × {q_found} = {p_found * q_found}")
    
    if p_found * q_found == n:
        print("Factorization successful!")
        
        # recover private key
        hacked_key = get_private_key(n, e, p_found, q_found)
        print(f"\nRecovered private key d = {hacked_key[1]}")
        
        # decrypt the message
        print("\nDecrypting message with hacked key...")
        hacked_msg = decrypt(encrypted, hacked_key)
        print(f"Decrypted message: {hacked_msg}")
        
        if hacked_msg == message:
            print("\nHACK SUCCESSFUL! Quantum computers will break RSA!")
        else:
            print("\nDecryption failed, something went wrong!")
    else:
        print("Factorization failed! This shouldn't happen with small numbers.")

# run the demo
if __name__ == "__main__":
    main()