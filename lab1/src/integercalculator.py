from constants import SIZE, FRACTION_PRECISION, INTEGER_SIZE

def int_to_direct_binary(n):
    bits = [0] * SIZE
    if n < 0:
        bits[0]=1
        n = abs(n)
    for i in range(SIZE - 1, 0, -1):
        bits[i] = n%2
        n = n // 2
        if not n:
            break
    return bits
    
def int_to_reverse_binary(n):
    bits = int_to_direct_binary(n)
    if bits[0] == 1:
        return reverse(bits)
    return bits
    
def reverse(bits):
    new_bits = bits
    for i in range(1, len(bits)):
        new_bits[i] = 1 - bits[i]
    return new_bits

def int_to_additional_binary(n):
    bits = int_to_reverse_binary(n)
    if bits[0] == 1:
        bits = add_bit(bits)
    return bits

def direct_to_additional(bits):
    if bits[0] == 1:
        bits = reverse(bits)
        return add_bit(bits)
    return bits

def add_bit(bits):
    for i in range(len(bits) - 1, -1, -1):
        if bits[i] == 1:
            bits[i] = 0
        else:
            bits[i] = 1
            break
    return bits

def binary_add(bits1, bits2):
    bits = add_bits(bits1, bits2)
    return bits[len(bits) + 1 - SIZE:]

def add_bits(bits1, bits2):
    i, j = len(bits1) - 1, len(bits2) - 1
    carry = 0
    bits = []
    while i >= 0 or j >= 0 or carry:
        val1 = bits1[i] if i >= 0 else 0
        val2 = bits2[j] if j >= 0 else 0

        total = val1 + val2 + carry

        new_digit = total % 2
        
        carry = total // 2

        bits.append(new_digit)

        i -= 1
        j -= 1

    return bits[::-1]

def additional_binary_to_int(bits):
    sign = bits[0]
    if sign:
        bits = add_bit(reverse(bits))
        sign = True
    val = 0
    for i in range(1, len(bits)):
        val = val * 2 + bits[i]
    return (-1)**sign * val

def direct_binary_to_int(bits):
    sign = bits[0]
    val = 0
    for i in range(1, len(bits)):
        val = val * 2 + bits[i]
    return (-1)**sign * val

def binary_sub(bits1, bits2):
    bits2[0] = 1 - bits2[0]
    bits2 = add_bit(reverse(bits2))
    return binary_add(bits1, bits2)

def binary_comp(bits1, bits2):
    if not any(bits1) or not any(bits2):
        return [0] * SIZE
    result = [0] * SIZE
    for i in range(SIZE - 1, 0, -1):
        if bits2[i] == 1:
            shifted_bits = shift_left(bits1, SIZE-i-1)
            result = binary_add(result, shifted_bits)
    result[0] = (bits1[0] + bits2[0]) % 2
    return result

def shift_left(bits, steps):
    if steps == 0:
        return bits
    if steps >= len(bits):
        return [0]*len(bits)
    return bits[steps:] + [0]*steps

def binary_div_with_fraction(dividend, divisor):
    if not any(divisor):
        raise ValueError("Деление на ноль")
    sign_q = dividend[0]
    dividend[0] = 0
    sign_m = divisor[0]
    divisor[0] = 0

    first_one = dividend.index(1)
    dividend = dividend[first_one:]

    first_one = divisor.index(1)
    divisor = divisor[first_one:]

    quotient = []
    remainder = []
    
    for bit in dividend:
        remainder.append(bit)
        
        while len(remainder) > 1 and remainder[0] == 0:
            remainder.pop(0)

        if is_greater_or_equal(remainder, divisor):
            quotient.append(1)
            remainder = subtract_binary(remainder, divisor)
        else:
            quotient.append(0)
    
    if any(quotient):
        first_one = quotient.index(1)
        quotient = quotient[first_one:]

    if len(quotient) < INTEGER_SIZE:
        quotient = [0]*(INTEGER_SIZE-len(quotient)) + quotient

    while len(quotient) != SIZE - 1 :
        remainder.append(0)
        while len(remainder) > 1 and remainder[0] == 0:
            remainder.pop(0)

        if is_greater_or_equal(remainder, dividend):
            quotient.append(1)
            remainder = subtract_binary(remainder, divisor)
        else:
            quotient.append(0)

    sign = sign_m + sign_q - sign_m * sign_q
            
    return [sign] + quotient

def is_greater_or_equal(a, b):
    if len(a) > len(b): return True
    if len(a) < len(b): return False
    for bit_a, bit_b in zip(a, b):
        if bit_a > bit_b: return True
        if bit_a < bit_b: return False
    return True

def fixed_point_to_decimal(bits) -> float:
    int_part = 0
    for i in range(1, INTEGER_SIZE + 1):
        power = INTEGER_SIZE - i
        int_part += bits[i] * (2 ** power)

    frac_part = 0.0
    for i in range(INTEGER_SIZE + 1, SIZE):
        power = -(i - INTEGER_SIZE)
        frac_part += bits[i] * (2 ** power)

    total = float(int_part) + frac_part
    return total * (-1) ** bits[0]

def get_opposite_bin(bits):
    return [1 - bits[0]] + bits[1:]

def subtract_binary(a, b):
    res = []
    a_copy = list(a)
    b_padded = [0] * (len(a) - len(b)) + b
    
    for i in range(len(a_copy) - 1, -1, -1):
        if a_copy[i] >= b_padded[i]:
            res.insert(0, a_copy[i] - b_padded[i])
        else:
            j = i - 1
            while a_copy[j] == 0:
                a_copy[j] = 1
                j -= 1
            a_copy[j] = 0
            res.insert(0, 2 + a_copy[i] - b_padded[i])
    return res