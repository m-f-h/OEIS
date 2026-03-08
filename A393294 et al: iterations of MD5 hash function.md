# Functions related iterations of the MD5 hash function.

Concerned sequences:
* [A393294: Iteration numbers k such that MD5^{k}(128 bits of 0) is a record high value.](https://oeis.org/A393294)
* [A234849: Positions of records in iterated MD5 applied to empty string.](https://oeis.org/A234849)

## Introduction
The [MD5 (message digest) hash function](https://en.wikipedia.org/wiki/MD5#Algorithm) 
takes a message and returns a 128-bit digest hash value (often displayed as 32 hex digits). 
The messaage is split into chunks of 512 bits = sixteen 32-bit words. 
It is padded to a multiple of that length by appending
- one bit 1, then
- as many bits 0 as to reach a multiple of 512 minus 64 (i.e., 448 (mod 512) bits, or 56 (mod 64) byte),
- then 64 bit with the length of the original message, modulo $ 2^64 $ (in little endian:
  if the length was 1, the last four byte are 01, 00, 00, 00)

## Iterated MD5
Since the output is a 128-bit block, 
it makes sense to consider the input also as a number in the range from 0 to $ 2^128 - 1 $.
However, these numbers can be considered either as messages of fixed length of 128 bit, 
or as messages of their "natural" length (bit_length).


```
import hashlib

def md5_128bit_number(number):
    """
    Takes an integer, treats it as a 128-bit block (Big Endian), 
    and returns the MD5 hash.
    """
    try:
        # Convert the integer to 16 bytes (128 bits).
        # 'big' means the most significant bit comes first (standard math notation).
        # If the number is 0, this creates 16 bytes of 0x00.
        message_bytes = number.to_bytes(16, byteorder='big') // big is the default
        
        # Calculate MD5
        return hashlib.md5(message_bytes).hexdigest()
    
    except OverflowError:
        return "Error: Number is too large to fit in 128 bits."

def hash2num(hex_string): return int(hex_string, 16)

# --- Test Cases ---

# Case 1: The "128 bits of 0"
# Input: Integer 0
for txt,val in { "0":0, "2^127":2**127, "1": 1,
             }.items():
        print(f"MD5({txt}):", hd := md5_128bit_number(val),"=", int(hd,16))

# Case 2: The "1 followed by 127 zeros" (2^127)
# This creates the byte string: 80 00 00 ... (0x80 is binary 10000000)
# Case 3: Just to show '1' is 00...01

from hashlib import md5

def A393294_gen1(starting_value: int = 0): # optional alt. starting value
    record = -1 ; msg = starting_value.to_bytes(16, byteorder='big')
    for i in range(1<<63): # sys.maxint
        if int.from_bytes(msg) > record:
            record = int.from_bytes(msg); yield i
        msg = md5(msg).digest()

def A393294_gen(starting_value: int = 0): # optional alt. starting value
    record = b''
    msg = starting_value.to_bytes(16, byteorder='big')
    for i in range(1<<63): # sys.maxint
        if msg > record:
            record = msg; yield i
        msg = md5(msg).digest()

#print(seq := [an for an, i in zip(A393294_gen(), range(10))] )


class A393294:
    i, max, msg, terms = 0, b'', (0).to_bytes(16), []
    def __new__(cls, n: int = None):
        return super().__new__(cls) if n is None else cls.__getitem__(cls, n)
    def __getitem__(A, n):
        while len(A.terms) <= n:
            while A.max >= A.msg:
                A.i += 1; A.msg = md5(A.msg).digest()
            A.max = A.msg; A.terms.append(A.i)
        return A.terms[n]
    
print([A393294(n) for n in range(10)])

def a393294(n = None, first = 1<<53): # without n: generator
    if not hasattr(A := a393294, 'msg'):
        A.iter, A.max, A.msg, A.terms = 0, b'', (0).to_bytes(16), []
    if n is None: return(A(n)for n in range(first))
    while n >= len(A.terms):
        while A.max >= A.msg:
            A.iter += 1; A.msg = md5(A.msg).digest()
        A.max = A.msg; A.terms.append(A.iter)
    return A.terms[n]

print(list(a393294(first=10)))
```
