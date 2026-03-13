from constants import SIZE, FRACTION_PRECISION, INTEGER_SIZE

def int_to_direct_binary(n):
    if not isinstance(n, int):
        raise ValueError
    bits = [0]*SIZE
    if n<0:
        bits[0]=1
        n = abs(n)
    for i in range(SIZE - 1, 0, -1):
        bits[i] = n%2
        n = n // 2
    return bits

def bin_to_str(bits):
    return "".join(str(i) for i in bits)
    
def int_to_reverse_binary(n):
    bits = int_to_direct_binary(n)
    if bits[0] == 1:
        return reverse(bits)
    return bits
    
def reverse(bits):
    for i in range(1, SIZE, 1):
        bits[i] = 1 - bits[i]
    return bits

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
    for i in range(SIZE - 1, -1, -1):
        if bits[i] == 1:
            bits[i] = 0
        else:
            bits[i] = 1
            break
    return bits

def binary_add(bits1, bits2):
    carry = 0
    bits = [0]*SIZE
    for i in range(SIZE - 1, -1, -1):
        # if bits1[i] == bits2[i]:
        #     if bits1[i] == 0:
        #         bits[i] = carry
        #         carry = 0
        #     else:
        #         bits[i] = carry
        #         carry = 1
        # else:
        #     if carry == 0:
        #         bits[i] = 1
        #     else:
        #         bits[i] = 0
        bit = bits1[i] + bits2[i] + carry
        bits[i] = bit % 2
        carry = bit // 2
    return bits

def additional_binary_to_int(bits):
    sign = bits[0]
    if sign:
        bits = add_bit(reverse(bits))
        sign = True
    val = 0
    for i in range(1, SIZE):
        val = val * 2 + bits[i]
    return (-1)**sign * val

def direct_binary_to_int(bits):
    sign = bits[0]
    val = 0
    for i in range(1, SIZE):
        val = val * 2 + bits[i]
    return (-1)**sign * val

def binary_sub(bits1, bits2):
    if bits2[0] == 1:
        bits2 = add_bit(reverse(bits2))
        bits2[0] = 0
    else:
        bits2[0] = 1
        bits2 = reverse(bits2)
        bits2 = add_bit(bits2)
    
    return binary_add(bits1, bits2)

def binary_comp(bits1, bits2):
    result = [0]*SIZE
    for i in range(SIZE - 1, 0, -1):
        if bits2[i] == 1:
            shifted_bits = shift_left(bits1, SIZE-i-1)
            result = binary_add(result, shifted_bits)
    result[0] = 0 if bits1[0]==bits2[0] else 1
    return result

def shift_left(bits, steps):
    if steps == 0:
        return bits
    if steps >= len(bits):
        return [0]*len(bits)
    return bits[steps:] + [0]*steps

def binary_div(q, m):
    if not any(m):
        raise ValueError("Деление на ноль")
    # q = int_to_direct_binary(abs(a1))
    # m = int_to_direct_binary(abs(b))
    sign_q = q[0]
    q[0] = 0
    sign_m = m[0]
    m[0] = 0

    a = [0]*SIZE
    for _ in range(SIZE - 1):
        a = shift_left_with_insert(a, q[1])
        a_sub = binary_sub(a, m.copy())
        if a_sub[0] == 0:
            q = shift_left_with_insert(q, 1)
            a = a_sub
        else:
            q = shift_left_with_insert(q, 0)
    sign = (sign_q + sign_m) % 2

    a = divide_fraction(a, m)
    
    return [sign] + q[SIZE-INTEGER_SIZE:] + a

def divide_fraction(bits, m):
    fractional_bits = []
    # m = int_to_direct_binary(abs(b))
    current_remainder = bits
    
    for _ in range(FRACTION_PRECISION):
        current_remainder = shift_left_with_insert(current_remainder, 0)
        
        sub_res = binary_sub(current_remainder, m.copy())
        
        if sub_res[0] == 0:
            fractional_bits.append(1)
            current_remainder = sub_res
        else:
            fractional_bits.append(0)

    return fractional_bits

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
    return -total if bits[0] == 1 else total

def shift_left_with_insert(bits, bit):
    return [0] + bits[2:] + [bit]