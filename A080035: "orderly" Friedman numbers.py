""" A080035: "orderly" Friedman numbers: 
    Friedman numbers (A036057) where the construction digits are used in the proper order.
DATA: 127, 343, 736, 1285, 2187, 2502, 2592, 2737, 3125, 3685, 3864, 3972, 4096, 6455, 11264, 11664, 12850, 13825, 14641, 15552, 15585, 15612, 15613, 15617, 15618, 15621, 15622, 15623, 15624, 15626, 15632, 15633, 15642, 15645, 15655, 15656

Numbers that can be written using their own digits and + - * / ^ ( ).
Example: 16387 = (1-6/8)^(-7)+3  (<=> 163

We need fractions and roots => sympy (?)

    *** UNFINISHED WORK IN PROGRESS ***
"""

def is_A080035(n, digits=None):
  """Return True iff n >= 0 can be written using the given string of digits, which defaults to str(n).
  In that case (digits not given) the decomposition must be nontrivial."""
  if not digits: digits=str(n) # n is assumed to be >= 0
  elif int(digits)==n: return True

  if len(digits) < 3:
    # in case of one single digit: we already checked that it's not equal (or trivial solution not allowed)
    if len(digits) < 2: return False
    a, b = map(int, digits)
    return (abs(n-a) == b or n+a == b or n == a*b or n*b == a 
            or n == a**b or n*a**b == 1)

  # first some simple cases:
  if n < 2:
    if n==0:
      # 0 = 0*anything, and 0 = difference of two consecutive equal digits
      if '0' in digits or any(a==b for a,b in zip(digits,digits[1:])):
        return True
      # we will test for less trivial solutions further down
    elif n==1: 
      # 1 = anything^0 where 0 can be diff. of two consec.equal digits
      if '0' in digits[1:] or any(a==b for a,b in zip(digits[1:],digits[2:])):
        return True
  
  # Now split up digits in two parts and check whether they can be combined to give n:
  for split_point in range(1, len(digits)-1):
    da = digits[:split_point] ; a = int(da)
    db = digits[split_point:] ; b = int(db)
    
    if (is_A080035(abs(n-b), da) or b and is_A080035(n+b, da) # n = +-(a) +- b
        or is_A080035(n/b, da) or b and is_A080035(n*b, da)  # n = (a) * b; n = (a)/b
        or notb and (is_A080035(n**(l/b), da) or is_A080035(n**(-1/b), da) # n = (a)^(+-b)
    
