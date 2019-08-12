from random import randint
import math

# generate random prime function
def generate_prime():
    T=10
    x = randint(2**(T-1), 2**T-1)
    while True:
        if is_prime(x):
            break
        else:
            x+=1
    return x

# primality check function
def is_prime(x):
    i = 2
    root = math.sqrt(x)
    while i < root:
        if x % i == 0:
            return False
        i += 1
    return True

# function to find gcd
def gcd(a, b):
    while b:
        a, b = b, a%b
    return a

# function to find extended gcd
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

# function to find modular inverse
def modinv(a,m):
    g,x,y = egcd(a,m)
    if g != 1:
        return None
    else:
        return x%m

if __name__ == "__main__":
    # choose 2 distinct primes p & q
    p = generate_prime()
    while True:
        q = generate_prime()
        if q != p:
            break
    print("p =",p)
    print("q =",q)
    n=p*q
    phi=(p-1)*(q-1)
    # Choose 1 < e < phi, which is coprime to phi which e is public key exponent
    e = randint(2,phi)
    e+=(1-e%2) # e must be odd
    while True:
        if gcd(e,phi)==1:
            break
        else:
            e+=2
    print("e =",e)
    # Compute d, the modular multiplicative inverse of e
    # Private key exponent d
    d = modinv(e, phi)
    print("d=",d)
    m = int(input("Enter message: "))
    c = (m**e) % n
    print("Encrypted message =",c)
    m1 = (c**d) % n
    print("Decrypted message =",m1)
