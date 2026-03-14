from constants import (
    SIZE
)

def int_to_5421(a):
    if a < 0 or a >= 10 ** (SIZE / 4):
        raise ValueError()

    a_str = str(a).zfill(SIZE // 4)

    bits = []
    for i in a_str:
        bits += num_to_5421(int(i))
    return bits

def from_binary_to_int(bits):
    val = 0
    for i in range(4):
        val = val * 2 + bits[i]
    return val

def add_binary4(bin1, bin2, carry = 0):
    result = []

    for i in range(3, -1, -1):
        val1 = bin1[i]
        val2 = bin2[i]

        total = val1 + val2 + carry

        new_digit = total % 2
        
        carry = total // 2

        result.append(new_digit)

    return result[::-1], carry

def dec_to_5421(n: int) -> int:
    if n < 5:
        return n
    else:
        return 8 + (n - 5) 

def num_to_5421(a):
    bits = [0] * 4
    a = dec_to_5421(a)
    for i in range(3, -1, -1):
        bits[i] = a%2
        a = a // 2
    return bits
    
def add_5421_bcd(bits1, bits2):
    carry = 0
    correction = 0
    result = [0]*SIZE
    for i in range(7, -1, -1):
        b1 = bits1[i*4:(i+1)*4]
        b2 = bits2[i*4:(i+1)*4]

        sum, carry = add_binary4(b1, b2, carry)
        
        sum_dec = from_binary_to_int(sum) 
        if(4 < sum_dec < 8 or sum_dec > 12):
            sum, correction = add_binary4(sum, [0, 0, 1, 1])
        if correction:
            carry = 1
            correction = 0
        result = [0]*(i)*4 + sum + result[(i+1)*4:]
    
    return result

def bcd_5421_to_num(bits):
    return bits[0]*5+bits[1]*4+bits[2]*2+bits[3]

def bcd_5421_to_int(bits):
    result = []
    for i in range(7, -1, -1):
        num = bits[i*4:(i+1)*4]
        num = bcd_5421_to_num(num)
        result.append(num)
    
    result_str = ""
    for i in reversed(result):
        result_str += str(i)

    return int(result_str)