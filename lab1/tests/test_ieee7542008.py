import pytest
from src.ieee7542008 import (
    from_float_to_ieee, from_ieee_to_float, add_ieee, sub_ieee,
    comp_ieee, div_ieee, get_integer_part_bits,
    get_fractional_part_bits, normalize,from_bits_to_int,
    pack, unpack, is_greater_or_equal
)
from constants import (
    SIZE, MANTISSA_SIZE, EXPONENT_SIZE
)

class TestNormalize:
    def test_with_integer_part(self):
        e, m = normalize([1,0,1], [1,0,1])
        assert e == 2 
        assert m[:3] == [0,1,1] 
    
    def test_without_integer_part(self):
        e, m = normalize([], [0,0,1,1]) 
        assert e == -3  
    
    def test_mantissa_padding(self):
        e, m = normalize([1], [])
        assert len(m) == MANTISSA_SIZE


class TestFromBitsToInt:
    @pytest.mark.parametrize("bits, expected", [
        ([0], 0), ([1], 1), ([1,0], 2), ([1,0,1], 5),
        ([1]*8, 255), ([0]*32, 0),
    ])
    def test_conversions(self, bits, expected):
        assert from_bits_to_int(bits) == expected


class TestFromFloatToIeee:
    def test_zero(self):
        result = from_float_to_ieee(0.0)
        assert result == [0] * SIZE
    
    def test_positive_one(self):
        result = from_float_to_ieee(1.0)
        assert result[0] == 0 
        assert result[1:9] == [0,1,1,1,1,1,1,1]
    
    def test_negative_number(self):
        result = from_float_to_ieee(-2.5)
        assert result[0] == 1  # sign bit
    
    def test_result_length(self):
        for val in [0.0, 1.0, -3.25]:
            result = from_float_to_ieee(val)
            assert len(result) == SIZE
            assert all(b in (0,1) for b in result)


class TestFromIeeeToFloat:
    def test_zero(self):
        assert from_ieee_to_float([0]*SIZE) == 0.0
    
    def test_one(self):
        bits = from_float_to_ieee(1.0)
        result = from_ieee_to_float(bits)
        assert abs(result - 1.0) < 1e-6
    
    @pytest.mark.parametrize("val", [2.0, 0.5, -3.14, 1e2, 1e-2])
    def test_roundtrip(self, val):
        if SIZE != 32:
            pytest.skip("Only 32-bit tested with struct")
        bits = from_float_to_ieee(val)
        result = from_ieee_to_float(bits)
        assert abs(result - val) / abs(val) < 1e-5 if val != 0 else abs(result) < 1e-10


class TestUnpackPack:
    def test_unpack_structure(self):
        bits = [0] + [1]*EXPONENT_SIZE + [1,0] + [0]*(MANTISSA_SIZE-2)
        s, e, m = unpack(bits)
        assert s == 0
        assert e == (2**EXPONENT_SIZE - 1)
        assert len(m) == MANTISSA_SIZE + 1
    
    def test_pack_unpack_roundtrip(self):
        original = [0] + [0,1,1,1,1,1,1,1] + [1,0,1] + [0]*(MANTISSA_SIZE-3)
        s, e, m = unpack(original)
        packed = pack(s, e, m)
        assert len(packed) == SIZE


class TestAddIeee:
    @pytest.mark.parametrize("a, b", [(1.0, 1.0), (2.5, 1.5), (0.1, 0.2)])
    def test_basic_addition(self, a, b):
        if SIZE != 32:
            pytest.skip("Only 32-bit with struct comparison")
        bits_a = from_float_to_ieee(a)
        bits_b = from_float_to_ieee(b)
        result_bits = add_ieee(bits_a, bits_b)
        result_val = from_ieee_to_float(result_bits)
        expected = a + b
        assert abs(result_val - expected) / abs(expected) < 1e-4 if expected != 0 else abs(result_val) < 1e-10
    
    def test_add_with_zero(self):
        bits_val = from_float_to_ieee(3.25)
        bits_zero = [0]*SIZE
        result = add_ieee(bits_val, bits_zero)
        assert from_ieee_to_float(result) == 3.25
    
    def test_result_properties(self):
        a = from_float_to_ieee(1.5)
        b = from_float_to_ieee(2.5)
        result = add_ieee(a, b)
        assert len(result) == SIZE
        assert all(b in (0,1) for b in result)


class TestSubIeee:
    def test_subtract_same(self):
        bits = from_float_to_ieee(5.0)
        result = sub_ieee(bits, bits.copy())
        assert from_ieee_to_float(result) == 0.0


class TestDivIeee:
    def test_division_by_zero_raises(self):
        bits_val = from_float_to_ieee(5.0)
        bits_zero = [0]*SIZE
        with pytest.raises(ValueError):
            div_ieee(bits_val, bits_zero)
    
    def test_divide_by_one(self):
        bits_val = from_float_to_ieee(7.5)
        bits_one = from_float_to_ieee(1.0)
        result = div_ieee(bits_val, bits_one)
        assert abs(from_ieee_to_float(result) - 7.5) < 1e-5
    
    @pytest.mark.parametrize("a, b", [(8.0, 2.0), (10.0, 4.0)])
    def test_basic_division(self, a, b):
        if SIZE != 32:
            pytest.skip("Only 32-bit")
        bits_a = from_float_to_ieee(a)
        bits_b = from_float_to_ieee(b)
        result = div_ieee(bits_a, bits_b)
        result_val = from_ieee_to_float(result)
        expected = a / b
        assert abs(result_val - expected) / abs(expected) < 1e-3 if expected != 0 else abs(result_val) < 1e-10


class TestCompIeee:
    def test_returns_valid_bits(self):
        a = from_float_to_ieee(2.0)
        b = from_float_to_ieee(3.0)
        result = comp_ieee(a, b)
        assert len(result) == SIZE
        assert all(bit in (0,1) for bit in result)


class TestIsGreaterOrEqual:
    @pytest.mark.parametrize("a, b, expected", [
        ([1,0,0], [0,1,1], True),
        ([0,1,1], [1,0,0], False),
        ([1,0,1], [1,0,1], True),
        ([0,0,1], [0,1], True),
    ])
    def test_comparisons(self, a, b, expected):
        assert is_greater_or_equal(a, b) == expected
