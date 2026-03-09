---
title: "Sequences and functions related to the MD5 hash function"
permalink: A393294/
---
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
- then, in the remaining 64 bit, the length of the original message, modulo $ 2^64 $
  (in little endian, so if the length was 1, the last four bytes are 01, 00, 00, 00).

Through repeated XOR and other bitwise operations, the MD5 algorithm computes one single 128-bit "digest" hash value
from the arbitrary number of 512-bit blocks. 
These 128 bits or 16 bytes are the resulting output message or return value of the MD5 function.

## Iterated MD5
The MD5 function can then be iterated by feeding it the 128-bit hash return value as new input.

Although it can be interpreted as an integer between 0 and $ 2^128 - 1 $, 
and this integer could be encoded using less bits if it has leading zeros
(for example, as a message of length given by `int.bit_length()`),
it seems most natural to consider the output as a fixed-width 128 bit integer,
when it is used as input on the next iteration.

Some sequences, however, such as [A234849](http://oeis.org/A234849), 
consider for example the empty string as input value
(which famously results in the return value 0xd41d8cd98f00b204e9800998ecf8427e).

So it is not excluded to consider values smaller than $ 2^127 $ as input messages of less bits.
However, many MD5 libraries do not allow to apply the MD5 function to messages whose length is not a multiple of 8 bits,
*i.e.*, not a sequence of bytes.
(TODO: check whether Python's hashlib would allow to compute MD5 for messages of such length.)

The subsequent Python code fragments allow to illustrate the corresponding conversions.
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

##### sequence A393294 #####
This sequence lists the iteration numbers k >= 0 such that MD5^k(128 bits 0) yields a new record high.
By convention, the initial value a(1) = 0.

from hashlib import md5

# first version of a generator
# this is obsolete, it does a "useless"/unnecessary conversion of 128-bit "messages"
# to integers, in oder to compare them.

def A393294_gen1(starting_value: int = 0): # optional alt. starting value
    record = -1 ; msg = starting_value.to_bytes(16, byteorder='big')
    for i in range(1<<63): # sys.maxint
        if int.from_bytes(msg) > record:
            record = int.from_bytes(msg); yield i
        msg = md5(msg).digest()

# The following better version only uses the 128 bit blocks (actually, 16-byte blocks)
# and an empty block as initial values

def A393294_gen(starting_value: int = 0): # optional alt. starting value
    record = b''
    msg = starting_value.to_bytes(16) #, byteorder='big') = default
    for i in range(1<<63): # sys.maxint
        if msg > record:
            record = msg; yield i
        msg = md5(msg).digest()

#print(seq := [an for an, i in zip(A393294_gen(), range(10))] )

class A393294:
    """This class can be used as well as a function A393294(n) that yields one specific term
of the sequence, or as an infinite generator `seq = A393294()` that can be used as iterator
and also be indexed to get again a specific term, through `seq[n]`."""
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

def a393294(n = None, first = 1<<53): # use 1<<53 for "infinite" - it will take infinitely long to compute even a(99) or so.
    """Return a(n) if `n` is given, or a generator if the `first` initial terms
if `first` is given, or else of the entire infinite sequence."""
    if not hasattr(A := a393294, 'msg'): # initialization
        A.iter, A.max, A.msg, A.terms = 0, b'', (0).to_bytes(16), []
    if n is None: return(A(n)for n in range(first))
    while n >= len(A.terms):
        while A.max >= A.msg: A.msg = md5(A.msg).digest(); A.iter += 1
        A.max = A.msg; A.terms.append(A.iter)
    return A.terms[n]

print(list(a393294(first=10)))
```
Possible alternate sequences:
* complement to A234849: start with "", list iteration numbers for which new record *lows* occur.
* complement to A393294: start with 128 bits 1, list iteration numbers for which new record *lows* occur.
* ... 

def A_gen(starting_value: int = 2**128-1): # optional alt. starting value
    record = b'\xff'*17 ; msg = starting_value.to_bytes(16) #, byteorder='big') = default
    for i in range(1<<63): # sys.maxint
        if msg < record: record = msg; print(i, msg); yield i
        msg = md5(msg).digest()

print(seq := [an for an,i in zip(A_gen(), range(10))] )
