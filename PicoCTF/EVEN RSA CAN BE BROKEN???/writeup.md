<h1>EVEN RSA CAN BE BROKEN???</h1>

From: https://play.picoctf.org/practice/challenge/470

Author: Michael Crotty

Description: This service provides you an encrypted flag. Can you decrypt it with just N & e?

<h2>General Functionality</h2>

A netcat session is provided `nc verbal-sleep.picoctf.net 53723` and the programs source code can be downloaded from the challenge.

<details>
  <summary>[Source Code]
  </summary>
  
```
from sys import exit
from Crypto.Util.number import bytes_to_long, inverse
from setup import get_primes

e = 65537

def gen_key(k):
    """
    Generates RSA key with k bits
    """
    p,q = get_primes(k//2)
    N = p*q
    d = inverse(e, (p-1)*(q-1))

    return ((N,e), d)

def encrypt(pubkey, m):
    N,e = pubkey
    return pow(bytes_to_long(m.encode('utf-8')), e, N)

def main(flag):
    pubkey, _privkey = gen_key(1024)
    encrypted = encrypt(pubkey, flag) 
    return (pubkey[0], encrypted)

if __name__ == "__main__":
    flag = open('flag.txt', 'r').read()
    flag = flag.strip()
    N, cypher  = main(flag)
    print("N:", N)
    print("e:", e)
    print("cyphertext:", cypher)
    exit()
```
  
</details>

When connecting to the session, the following output is provided:
```
N: 21221630957976754214970783847742502065216812838679803732723052101692065654802835928739864576541365042832832333147154528905382496245223133324395030303392946
e: 65537
cyphertext: 14122001083690314114019355481318783590691539592666625208730273551862687121567174034584226311975431224378334933816636723598193649527456758876648464108277553
```

<h2>Experiementation and research</h2>

From the source code, it seems that if we were to understand and reverse the key generation and encryption functions, we might be able to mathematically deduce what the source message was. 

What we know based on the information provided:

```
e = 65537
p, q = get_primes(512)
N (the multiplication of prime factors (p,q) of 512) = 21221630957976754214970783847742502065216812838679803732723052101692065654802835928739864576541365042832832333147154528905382496245223133324395030303392946
KeyLength = 1024 bits
```

IF we can reverse the `inverse(e, (p-1)*(q-1))` function then we can retrieve the private key.

Then, I imagine that we can use this private key to decrypt the message by inverting the `pow(bytes_to_long(m.encode('utf-8')), e, N)`. Without doing any reading on this, I'm not sure where to start in terms of reverse the encryption function... so lets get reading!

First however, lets install some of these encryption libraries:

`pip install pycryptodome` and `pip install crypto`.
![image](https://github.com/user-attachments/assets/485516da-0f39-4d80-9454-e899d04ec5f3)

Key takeaways and notes from: **How to break RSA encryption | Computerphile video:** https://youtu.be/-ShwJqAalOk
<details>
  <summary> Notes taken during video
  </summary>
  
- Sign something using private key (d) (hiddne information)
- Verify the signiture using the public key (e, N) (public information).
- E is usually 65537
- N is calculating p * q which are prime numbers that are randomly generated. N can be multiple thousand bits long.
- Its possible that weak values for p and q can be found when a bad library is used to generate these random numbers
- Once we know p and q, we can calculate Euler's Totient which is = (p-1) * (q-1).
- e * d is congruent to 1 (mod totient(N)
- We want to find some number which when we multiply by e we get an intermediate value which when we reduce by the mod we get 1 again. If we find this then we would have found the private key.
- There exist other ways to calcualte the totient of N, IE brute foce, but this is unrealistic computationally.
- The fastest alternative is to factor N into p and q.
- Fermats factorisation algorithm can be used to break down p and q.
- N = a^2 - b^2 = (a+b)(a-b)
- b^2 = a^2 - N
- Let then test the sqrt(all integers of a squared minus N) the result when sqrt'd needs to be an integer and if it isn't we test the next integer (+1)
- Once you discover 'a' and 'b', you can do (a+b)(a-b) to get p and q which can then be used to calculate the private key.
</details>

Next step:
- Create python program to break primes using Fermats factorisation algorithm. https://en.wikipedia.org/wiki/Fermat's_factorization_method
![image](https://github.com/user-attachments/assets/5603ef36-beb4-4087-bfdd-cacb46f05148)

Hold your horses, I've been overthinking everything.

![image](https://github.com/user-attachments/assets/ae2e8952-201a-402a-adfc-611feef0d209)


<h2>The correct approach</h2>

This N value is even, and we can prove that for all integers, an odd integer multiplied by an odd integer is odd.

IE, for all x, y in the integers, suppose x and y are odd. Thus x = 2k + 1 and y = 2m + 1 for some k, m in the integers. 

Therefore the product x*y is equivalent to (2k+1)(2m+1) = 4km + 2k + 2m + 1 = 2(km + k + m) + 1

Since (km + k + m) will be in the integers, this shows thats any product of odd integers is odd.

Thus, for the N value to be even, this means that one of the p or q primes must be even. And there is only one even prime number, 2.

Therefore the p and q values are p = 2 and q = N // 2.
```
p = 2
q = 10610815478988377107485391923871251032608406419339901866361526050846032827401417964369932288270682521416416166573577264452691248122611566662197515151696473
```

Next step:
Recreate the decryption process by finding the private key.

The following code annotates the elements of RSA encryption and and demonstrates the encryption and decryption of the number 123456789:

```
from Crypto.Util.number import bytes_to_long, inverse

# e is smaller than the totient(n) and is comprime with it, public information
e = 65537

#  p is a random prime number, private information
p = 10610815478988377107485391923871251032608406419339901866361526050846032827401417964369932288270682521416416166573577264452691248122611566662197515151696473

# q is a random prime number, private information
q = 2

# N is the product of p and q. public information
N = p * q

# d is the private key derived from the inverse of e mod totient(n), private information
d = inverse(e, (p-1)*(q-1))

publickey = (N, e)
privatekey = (N, d)

# example message
message = 123456789
print(f"Encrypting = {message}")

# pow function returns message^e mod N. Notice, we encrypt with the public key (N, e)
encrypted_m = pow(message, e, N)
print(f"New encryption value = {encrypted_m}")

# notice we decrypt with the private key (N, d)
decrypted_m = pow(encrypted_m, d, N)

print(f"Returned decrypted value = {decrypted_m}")
# Prints 123456789
```

When plugging my cipher text into the decoding stage of this code, I receive the integer 3030612722376619015339251852200174143198160267119133805409341331747709

Since this is an integer I will need to perform conversions on it to read it as a string and retrieve the flag. Generally when encrypting text the following processes are applied:
- The text is converted to hexadecimal byte sequences based on the character encoding (typically UTF-8).
- This sequence of hexadecimal numbers is combined by the computer to create one very large sequence of bits which can be represented as a single decimal. I believe this is what we're seeing.

Therefore in order to undo this encoding, we need to define a number of bytes we will return from the sequence. Then, we can use the python integer method .to_bytes() to convert an integer into a sequence of `x` bytes in the big-endian format. Lastly, now that we have our bytes sequence, we can decode these bytes using pythons bytes .decode() method and specifying the characterset utf-8.

```
def decimal_to_ascii(decimal_input: int) -> str:
    byte_length = (decimal_input.bit_length() + 7) // 8
    byte_sequence = decimal_input.to_bytes(byte_length, "big")
    output = byte_sequence.decode("utf-8")
    return output
```

And there we have it: `picoCTF{tw0_1$_pr!m33486c703}`

Whoopee!





Applications used during CTF:

- Kali Linux

- Mozilla Firefox

- Visual Studio Code

- Python 3.13 and Pycryptodome utilities


Core sources of information:

Wikipedia: https://en.wikipedia.org/wiki/Fermat's_factorization_method
  - Fermats Factorisation method

Youtube: https://youtu.be/-ShwJqAalOk
  - ComputerPhile | How to break RSA encryption
    
ChatGPT: https://chatgpt.com/
  - Clarification of the native pow() function and byte arrays.

Drexel RSA calculator: https://www.cs.drexel.edu/~popyack/IntroCS/HW/RSAWorksheet.html
  - Clarification regarding the mathematics and sequence used to derive keys, encrypt using powers+mod and decrypt using power+mod
