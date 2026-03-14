import pytest
from constants import SIZE, FRACTION_PRECISION, INTEGER_SIZE

from src.integercalculator import (
    int_to_direct_binary, int_to_reverse_binary, int_to_additional_binary,
    direct_to_additional, additional_binary_to_int, direct_binary_to_int,
    binary_add, binary_sub, binary_comp, binary_div_with_fraction,
    fixed_point_to_decimal, get_opposite_bin, shift_left
)

def bits_to_str(bits):
    return "".join(map(str, bits))

def generate_test_cases():
    """Генерирует набор чисел для тестирования, включая граничные значения."""
    max_val = 2 ** (INTEGER_SIZE - 1) - 1
    min_val = -(2 ** (INTEGER_SIZE - 1))
    
    cases = [
        0, 1, -1, 2, -2, 
        max_val, min_val, 
        max_val - 1, min_val + 1,
        42, -42, 127, -128
    ]

    return [x for x in cases if min_val <= x <= max_val]

class TestConversion:
    @pytest.mark.parametrize("n", generate_test_cases())
    def test_direct_conversion_roundtrip(self, n):
        bits = int_to_direct_binary(n)
        assert len(bits) == SIZE
        result = direct_binary_to_int(bits)
        assert result == n, f"Failed for {n}: got {result}, bits={bits_to_str(bits)}"

    @pytest.mark.parametrize("n", generate_test_cases())
    def test_additional_conversion_roundtrip(self, n):
        bits = int_to_additional_binary(n)
        assert len(bits) == SIZE
        result = additional_binary_to_int(bits)
        assert result == n, f"Failed for {n}: got {result}, bits={bits_to_str(bits)}"

    def test_zero_representations(self):
        zero_direct = int_to_direct_binary(0)
        zero_add = int_to_additional_binary(0)
        
        assert direct_binary_to_int(zero_direct) == 0
        assert additional_binary_to_int(zero_add) == 0
        assert zero_direct[0] == 0


class TestArithmetic:
    @pytest.mark.parametrize("a,b", [
        (5, 3), (5, -3), (-5, 3), (-5, -3),
        (0, 10), (10, 0), (0, 0),
        (2**(INTEGER_SIZE-2), 1),
        (-(2**(INTEGER_SIZE-2)), -1)
    ])
    def test_addition_via_additional_code(self, a, b):

        limit = 2**(INTEGER_SIZE-1)
        if not (-limit <= a+b < limit):
            pytest.skip("Overflow expected for this case")

        bits_a = int_to_additional_binary(a)
        bits_b = int_to_additional_binary(b)
        
        res_bits = binary_add(bits_a, bits_b)
        res_val = additional_binary_to_int(res_bits)
        
        assert res_val == a + b, f"{a}+{b} != {res_val}. Bits: {bits_to_str(res_bits)}"

    @pytest.mark.parametrize("a,b", [
        (10, 4), (4, 10), (0, 5), (5, 0),
        (-5, -2), (-5, 2), (5, -2)
    ])
    def test_subtraction(self, a, b):
        limit = 2**(INTEGER_SIZE-1)
        if not (-limit <= a-b < limit):
            pytest.skip("Overflow expected")

        bits_a = int_to_additional_binary(a)
        bits_b = int_to_additional_binary(b)
        
        res_bits = binary_sub(bits_a, bits_b)
        res_val = additional_binary_to_int(res_bits)
        
        assert res_val == a - b, f"{a}-{b} != {res_val}"

class TestMultiplication:
    @pytest.mark.parametrize("a,b", [
        (2, 3), (3, 2), (-2, 3), (2, -3), (-2, -3),
        (1, 10), (10, 1), (0, 5), (5, 0)
    ])
    def test_multiplication_basic(self, a, b):
        limit = 2**(INTEGER_SIZE-1)
        if not (-limit <= a*b < limit):
            pytest.skip("Result out of range for current SIZE")

        bits_a = int_to_additional_binary(a)
        bits_b = int_to_additional_binary(b)
        
        res_bits = binary_comp(bits_a, bits_b)
        res_val = additional_binary_to_int(res_bits)
        
        assert res_val == a * b, f"{a}*{b} != {res_val}"

class TestDivisionAndFixedPoint:
    def test_division_integer_result(self):

        dividend = int_to_additional_binary(10)
        divisor = int_to_additional_binary(2)
        
        res_bits = binary_div_with_fraction(dividend, divisor)
        res_val = fixed_point_to_decimal(res_bits)
        
        assert abs(res_val - 5.0) < 0.001

    def test_division_with_fraction(self):
        
        dividend = int_to_additional_binary(1)
        divisor = int_to_additional_binary(2)
        
        res_bits = binary_div_with_fraction(dividend, divisor)
        res_val = fixed_point_to_decimal(res_bits)
        
        assert abs(res_val - 0.5) < 0.001

    def test_division_by_zero(self):

        dividend = int_to_additional_binary(10)
        divisor = int_to_additional_binary(0)
        
        with pytest.raises(ValueError):
            binary_div_with_fraction(dividend, divisor)

class TestUtilities:
    def test_shift_left(self):
        bits = [0, 1, 0, 1, 0]
        shifted = shift_left(bits, 1)
        assert shifted == [1, 0, 1, 0, 0]
        
        shifted_zero = shift_left(bits, 0)
        assert shifted_zero == bits
        
        shifted_out = shift_left(bits, 10)
        assert shifted_out == [0] * len(bits)