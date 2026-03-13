from constants import SIZE, MANTISSA_SIZE, EXPONENT_SIZE

def from_float_to_ieee(num):
    if num == 0.0:
        return [0] * SIZE

    sign = 1 if num<0 else 0
    int_part = int(num)
    frac_part = num - int(num)

    int_bits = get_integer_bits(abs(int_part))
    frac_bits = get_fractional_bits(abs(frac_part))

    e, m = normalize(int_bits, frac_bits)
    
    e = get_integer_bits(e + 127)
    if len(e) < EXPONENT_SIZE:
        e = [0]*(EXPONENT_SIZE-len(e)) + e

    return [sign] + e + m

def get_integer_bits(int_part):
    bits = []
    while int_part > 0:
        bits.append(int_part % 2)
        int_part = int_part // 2
    return bits[::-1]

def get_fractional_bits(frac_part):
    bits = []
    for _ in range(SIZE):
        if frac_part == 0:
            return bits
        frac_part*=2
        bit = int(frac_part)
        bits.append(bit)
        frac_part -= bit
    return bits

def normalize(int_bits, frac_bits):
    if int_bits:
        e = len(int_bits) - 1
        m = int_bits[1:] + frac_bits
    else:
        first_one = frac_bits.index(1)
        e = -(first_one + 1)
        m = frac_bits[first_one + 1:]
    
    return e, m[:MANTISSA_SIZE] + [0] * (MANTISSA_SIZE - len(m))

def from_ieee_to_float(bits):
    s, e, m = unpack(bits)

    m_value = 0.0
    for i, bit in enumerate(m):
        m_value += bit * (2**(-i))       

    return (1 - 2 * s) * m_value * 2**(e-127)

def unpack(bits):
    sign = bits[0]
    e = bits[1:EXPONENT_SIZE+1]
    m = bits[EXPONENT_SIZE+1:]

    e_value = 0
    for i, bit in enumerate(reversed(e)):
        e_value += bit * 2**(i)

    if e_value == 0 and not any(m):
        return sign, 0, [0] * (MANTISSA_SIZE+1)

    #e_value -= 127

    return sign, e_value, [1] + m      

def pack(s, e, m):
    e = get_integer_bits(e)
    if len(e) < EXPONENT_SIZE:
        e = [0]*(EXPONENT_SIZE-len(e)) + e
    print(e)
    return [s] + e + m[1:MANTISSA_SIZE+1]

def from_bits_to_int(bits):
    num = 0
    for i, bit in enumerate(reversed(bits)):
        num += bit * (2 ** i)
    return num

def add_ieee(a, b):
    s1, e1, m1 = unpack(a)
    s2, e2, m2 = unpack(b)
    s = s1
    e = e1
    if e1 > e2:
        m2 = shift_right(m2, e1 - e2)
    elif e1 != e2:
        m1 = shift_right(m1, e2 - e1)
        e = e2
        s = s2
    if s1 == s2:
        m = add_mantissas(m1, m2)
    else:
        m = sub_mantissas(m1, m2)
    m, e = normalize_mantissa(m, e)
    return pack(s, e, m)

def normalize_mantissa(m, e):
    if not any(m):
        return m, e
    first_one = m.index(1)
    e = e - first_one
    m = m[first_one:]
    return m, e

def add_mantissas(m1, m2):
    m = []
    carry = 0
    for i in range(len(m1)-1, -1, -1):
        bit = m1[i] + m2[i] + carry
        m.append(bit % 2) 
        carry = bit // 2
    if carry == 1:
        m.append(1)
    m.reverse()
    return m

def sub_mantissas(m1, m2):
    for i in range(len(m1)):
        if m2[i]>m1[i]:
            m1, m2 = m2, m1
            break
    m = []
    borrow = 0
    for i in range(len(m1) - 1, -1, -1):
        bit = m1[i] - m2[i] - borrow
        if bit < 0:
            bit = 1
            borrow = 1
        else:
            borrow = 0
        m.append(bit)
    m.reverse()
    print(f"m = {m}")
    return m
    

def shift_right(bits, steps):
    if steps > MANTISSA_SIZE + 1:
        return [0] * (MANTISSA_SIZE + 1)
    new_bits = [0] * steps + bits[:-steps]
    return new_bits

def sub_ieee(a, b):
    b[0] = 1 - b[0]
    return add_ieee(a, b)

def comp_ieee(a, b):
    s1, e1, m1 = unpack(a)
    s2, e2, m2 = unpack(b)
    s = (s1 + s2) % 2
    e = e1 + e2 - 127
    m = []

    m1_reversed = m1[::-1]
    first_one = m1_reversed.index(1)
    m1_cutted = m1[:len(m1) - first_one]
    
    for i in range(len(m2)-1, -1, -1):
        if m2[i] == 1:
            m1_cutted_with_shift = m1_cutted + [0]*i
            m = add_binary(m, m1_cutted_with_shift) 
    print(m)
    return pack(s, e, m)
    # print(m)

    
def add_binary(bin1, bin2):
    i, j = len(bin1) - 1, len(bin2) - 1
    carry = 0
    result = []

    # Цикл пока есть цифры в обоих списках или остался перенос
    while i >= 0 or j >= 0 or carry:
        # Получаем текущие цифры (0 если индекс вышел за границы)
        val1 = bin1[i] if i >= 0 else 0
        val2 = bin2[j] if j >= 0 else 0

        # Сумма цифр и переноса
        total = val1 + val2 + carry

        # Новая цифра результата (остаток от деления на 2)
        # Используем математику вместо % для чистоты логики 0/1, хотя % допустим
        new_digit = 1 if total == 1 or total == 3 else 0
        
        # Новый перенос (если сумма >= 2)
        carry = 1 if total >= 2 else 0

        result.append(new_digit)

        i -= 1
        j -= 1

    return result[::-1]

def div_ieee(a, b):
    s1, e1, m1 = unpack(a)
    s2, e2, m2 = unpack(b)
    s = (s1 + s2) % 2
    e = e1 - e2 + 127
    
    if not any(m2):
        raise ValueError("Деление на ноль")

    if not any(m1):
        return pack(0, 0, [0]*24)
    
    m1_reversed = m1[::-1]
    first_one = m1_reversed.index(1)
    m1_cutted = m1[:len(m2) - first_one]

    m2_reversed = m2[::-1]
    first_one = m2_reversed.index(1)
    m2_cutted = m2[:len(m2) - first_one]

    m = binary_division(m1_cutted, m2_cutted)

    print(m)

    return pack(s, e, m)
    # print(m)

def binary_division(dividend: list[int], divisor: list[int], steps: int = 24):
    quotient = []  # Частное (результат)
    remainder = [] # Текущий остаток
    
    for bit in dividend:
        # 1. "Сносим" следующий бит из делимого в остаток
        remainder.append(bit)
        
        # Убираем ведущие нули в остатке для удобства сравнения
        while len(remainder) > 1 and remainder[0] == 0:
            remainder.pop(0)
            
        # 2. Сравниваем: помещается ли делитель в текущий остаток?
        # (Функция сравнения списков по величине числа)
        if is_greater_or_equal(remainder, divisor):
            quotient.append(1)
            remainder = subtract_binary(remainder, divisor)
        else:
            quotient.append(0)
            
    first_one = quotient.index(1)
    quotient = quotient[first_one:]

    # 3. После того как биты делимого кончились, продолжаем делить "в дробь"
    # Добавляем виртуальные нули (как запятую в столбике)
    while len(quotient) != 24:
        remainder.append(0)
        while len(remainder) > 1 and remainder[0] == 0:
            remainder.pop(0)

        if is_greater_or_equal(remainder, divisor):
            quotient.append(1)
            remainder = subtract_binary(remainder, divisor)
        else:
            quotient.append(0)
            
    return quotient

def is_greater_or_equal(a, b):
    # Сначала сравниваем длину (число без ведущих нулей)
    if len(a) > len(b): return True
    if len(a) < len(b): return False
    # Если длины равны, сравниваем побитово
    for bit_a, bit_b in zip(a, b):
        if bit_a > bit_b: return True
        if bit_a < bit_b: return False
    return True

def subtract_binary(a, b):
    # Обычное вычитание столбиком (a - b)
    res = []
    a_copy = list(a)
    b_padded = [0] * (len(a) - len(b)) + b
    
    for i in range(len(a_copy) - 1, -1, -1):
        if a_copy[i] >= b_padded[i]:
            res.insert(0, a_copy[i] - b_padded[i])
        else:
            # Занимаем у соседа
            j = i - 1
            while a_copy[j] == 0:
                a_copy[j] = 1
                j -= 1
            a_copy[j] = 0
            res.insert(0, 2 + a_copy[i] - b_padded[i])
    return res