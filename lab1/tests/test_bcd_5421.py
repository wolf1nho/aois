import pytest
from constants import (
    SIZE
)
from src.bcd5421 import (
    dec_to_5421, num_to_5421, from_binary_to_int, add_binary4, int_to_5421, bcd_5421_to_int, bcd_5421_to_num, add_5421_bcd
)

class TestDecTo5421:
    @pytest.mark.parametrize("n, expected", [
        (0, 0), (1, 1), (2, 2), (3, 3), (4, 4),
        (5, 8), (6, 9), (7, 10), (8, 11), (9, 12),
    ])
    def test_all_digits(self, n, expected):
        assert dec_to_5421(n) == expected


class TestNumTo5421:
    @pytest.mark.parametrize("digit, expected", [
        (0, [0,0,0,0]), (1, [0,0,0,1]), (2, [0,0,1,0]), (3, [0,0,1,1]),
        (4, [0,1,0,0]), (5, [1,0,0,0]), (6, [1,0,0,1]), (7, [1,0,1,0]),
        (8, [1,0,1,1]), (9, [1,1,0,0]),
    ])
    def test_digits_to_bits(self, digit, expected):
        assert num_to_5421(digit) == expected
    
    def test_returns_list_of_4_bits(self):
        result = num_to_5421(5)
        assert isinstance(result, list) and len(result) == 4
        assert all(b in (0, 1) for b in result)


class TestFromBinaryToInt:
    @pytest.mark.parametrize("bits, expected", [
        ([0,0,0,0], 0), ([0,0,0,1], 1), ([0,1,0,1], 5), ([1,1,1,1], 15),
    ])
    def test_conversions(self, bits, expected):
        assert from_binary_to_int(bits) == expected


class TestAddBinary4:
    @pytest.mark.parametrize("a, b, carry_in, exp_sum, exp_carry", [
        ([0,0,0,0], [0,0,0,0], 0, [0,0,0,0], 0),
        ([0,0,0,1], [0,0,0,1], 0, [0,0,1,0], 0),
        ([1,0,0,0], [1,0,0,0], 0, [0,0,0,0], 1),  
        ([1,1,1,1], [0,0,0,1], 0, [0,0,0,0], 1),  
        ([0,0,0,1], [0,0,0,1], 1, [0,0,1,1], 0), 
    ])
    def test_addition(self, a, b, carry_in, exp_sum, exp_carry):
        res_sum, res_carry = add_binary4(a, b, carry_in)
        assert res_sum == exp_sum and res_carry == exp_carry


class TestIntTo5421:
    def test_zero(self):
        result = int_to_5421(0)
        assert len(result) == SIZE and all(b == 0 for b in result)
    
    @pytest.mark.parametrize("num", [1, 42, 9999, 12345678])
    def test_valid_numbers(self, num):
        result = int_to_5421(num)
        assert len(result) == SIZE and all(b in (0,1) for b in result)
    
    def test_negative_raises(self):
        with pytest.raises(ValueError):
            int_to_5421(-1)
    
    def test_too_large_raises(self):
        with pytest.raises(ValueError):
            int_to_5421(10 ** (SIZE // 4))
    
    def test_padding(self):
        result = int_to_5421(42)
        assert result[24:28] == num_to_5421(4)
        assert result[28:32] == num_to_5421(2)


class TestBcd5421ToNum:
    @pytest.mark.parametrize("bits, expected", [
        ([0,0,0,0], 0), ([0,0,0,1], 1), ([1,0,0,0], 5), ([1,1,0,0], 9),
    ])
    def test_valid_codes(self, bits, expected):
        assert bcd_5421_to_num(bits) == expected


class TestBcd5421ToInt:
    def test_zero(self):
        assert bcd_5421_to_int([0]*SIZE) == 0
    
    def test_roundtrip(self):
        for num in [0, 1, 42, 9999, 12345678]:
            bits = int_to_5421(num)
            assert bcd_5421_to_int(bits) == num

class TestAdd5421Bcd:
    def _to_bits(self, n): return int_to_5421(n)
    def _to_int(self, b): return bcd_5421_to_int(b)
    
    @pytest.mark.parametrize("a, b", [(0,0), (1,2), (123,456), (9999,1)])
    def test_basic_addition(self, a, b):
        expected = (a + b) % (10 ** (SIZE//4))
        result = add_5421_bcd(self._to_bits(a), self._to_bits(b))
        assert self._to_int(result) == expected
    
    @pytest.mark.parametrize("a, b, expected", [
        (5, 5, 10), (9, 1, 10), (99, 1, 100), (7, 6, 13),
    ])
    def test_with_carry_and_correction(self, a, b, expected):
        max_d = 10 ** (SIZE//4)
        result = add_5421_bcd(self._to_bits(a), self._to_bits(b))
        assert self._to_int(result) == expected % max_d
    
    def test_result_properties(self):
        res = add_5421_bcd(self._to_bits(123), self._to_bits(456))
        assert len(res) == SIZE and all(b in (0,1) for b in res)


class TestRoundTrip:
    @pytest.mark.parametrize("num", [0, 1, 99, 9999, 12345678])
    def test_int_to_bcd_to_int(self, num):
        if num >= 10 ** (SIZE//4):
            pytest.skip("Out of range")
        bits = int_to_5421(num)
        assert bcd_5421_to_int(bits) == num