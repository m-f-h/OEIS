---
title: "Sequences and functions related to the MD5 hash function"
permalink: A393294/
---
## Functions related to iterations of the MD5 hash function.

Concerned sequences:
* [A234849: Positions of records in iterated MD5 applied to empty string.](https://oeis.org/A234849)
* [A393294: Iteration numbers k such that MD5^{k}(128 bits of 0) is a record high value.](https://oeis.org/A393294)

### Introduction
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

### Iterated MD5
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
```
### sequence A393294 
This sequence lists the iteration numbers k >= 0 such that MD5^k(128 bits 0) yields a new record high.
By convention, the initial value a(1) = 0.
```
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
## Possible alternate sequences:
* complement to A234849: start with "", list iteration numbers for which new record *lows* occur.\
  submitted as https://oeis.org/draft/A393133
```
# A393133: record lows, starting with 0 bits:
def A393133_gen(starting_value: int = 0): # optional alt. starting value
    record = b'\xff'*17 ; msg = b''#starting_value.to_bytes(16) #, byteorder='big') = default
    for i in range(1,1<<63): # sys.maxint
        msg = md5(msg).digest()
        if msg < record: record = msg; print(i, msg.hex()); yield i
print(seq := [an for an,i in zip(A_gen(), range(12))] )

def clz_bytes(b: bytes) -> int # count leading zeros
    #if not b: return 0
    i = int.from_bytes(b, "big")
    #if i == 0: return 8 * len(b)
    return 8 * len(b) - i.bit_length()
clz_bytes = lambda b: len(b)*8 - int.from_bytes(b, "big").bit_length()

[clz_bytes(b.to_bytes(16)) for a,b in Result33] # where result33 is the following:
```
Result: (k = A393133(n), MD5^k('')) = (   1, 0xd41d8cd98f00b204e9800998ecf8427e),
  (   2, 0x59adb24ef3cdbe0297f05b395827453f),
  (   4, 0x0a314fe6160e361429dd96a2b098126b),
  (  21, 0x07598b687b0613b109a1f54abff4800b),
  (  59, 0x05d645dc6fb19ab372419611795b8b45),
  (  62, 0x03cf36e12b2fbdf4909f79791a536532),
  (  77, 0x011f3916ecc7bd1dbb3e0373bb660a07),
  ( 225, 0x00ab4e5809b5d59ea6a2d5e029286956),
  ( 393, 0x0096e56c187563d2509cf015f8fd39a6),
  ( 478, 0x007aad42a2209f0b8d35d6d393ac0802),
  ( 604, 0x00339d9ed22867d3504730be404620bf),
  (3499, 0x0021c64cee10be8b9db0779154e7c70e),
  (3616, 0x0006dc6b1c1224a7849119a7ec1e7342),
 (39205, 0x00048cf06f4d919960cfc2d557b7a415),
 (41013, 0x000420c7a623f5c193fbaf8b5120056f),
 (44115, 0x00021b0519da23d8db5a6a8604f5b7fb),
(120180, 0x000182e3fabd6c55b60ff5be4c127e41),
(140309, 0x000127e3145a1d72ba5f8915e9b647f1),
(211937, 0x0000cae164c647bc7699e5412933bac9),
(213599, 0x00003ecc1a25ba0a882d5012d3f8d3e3),
(266973, 0x0000104f51d4759a146dd377e91a9a0c),
(763017, 0x0000002214338697e2b26e52e74fd11f), ...

* complement to A393294: start with 128 bits 1, list iteration numbers for which new record *lows* occur.\
  submitted as https://oeis.org/draft/A393134
```
# A393134: record lows, starting with 128 bits 1:
def A393134_gen(starting_value: int = 2**128-1): # optional alt. starting value
    record = b'\xff'*17 ; msg = starting_value.to_bytes(16) #, byteorder='big') = default
    for i in range(1<<63): # sys.maxint
        if msg < record: record = msg; print(i, msg); yield i
        msg = md5(msg).digest()

print(seq := [an for an,i in zip(A_gen(), range(10))] )
```
For the records, here are the hex representations of the record lows:
 ((a,b.hex())for a,b in res) = \
       (1, '8d79cbc9a4ecdde112fc91ba625b13c2'), (5, '43bb38f62f513fa28cf28a59d7512540'), 
       (7, '0b065300a3311ae95c43b45d0414d28f'), (42, '04ac12e0b34aff0ad4fb85ce49991bf6'), 
     (147, '0023b5149f0842a563334c2fe1953199'), (176, '001627f5de9615fb2191d3f0fe6eaa44'), 
    (3536, '0012dfe3be2189f5a1badd6925cc56b7'), (5866, '000b21673f479bb0835d7518dbcf13e4'), 
    (8099, '00058ec88240a1c9be957d797641fd9a'), (38939, '0000b1850cbc3a9da2a076fab4cd5f7a'), 
   (41788, '00000ce88696e96703e30a0921e8e27b'), (822951, '00000b6884ef416ed523f28ef71ebd46'), 
 (2971632, '0000084a3b17caaf5c20b165e9ffc31d'), (6665500, '0000001bec3cc044e45efcb77b316ef8')]

[clz_bytes(b) for a,b in res] # the 12 corresponds to a(8) = 5866 => '000b...'

=> [0, 1, 4, 5, 10, 11, 11, 12, 13, 16, 20, 20, 20, 27]
