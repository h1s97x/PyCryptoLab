"""测试基础设施工具函数"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from infrastructure.converters.TypeConvert import (
    is_hex_string,
    str_to_hex_list,
    int_to_str,
    hex_list_to_str,
    str_to_int,
    int_to_hex_list,
)


class TestIsHexString:
    """测试 is_hex_string 函数"""

    def test_valid_hex_lowercase(self):
        assert is_hex_string("abcdef123456") == 0

    def test_valid_hex_uppercase(self):
        assert is_hex_string("ABCDEF123456") == 0

    def test_valid_hex_mixed(self):
        assert is_hex_string("AbCdEf123456") == 0

    def test_invalid_hex_with_space(self):
        """空格不是有效的十六进制字符"""
        assert is_hex_string("AB CD EF 12 34 56") == 1

    def test_invalid_hex_with_g(self):
        assert is_hex_string("ABCDEFG12345") == 1

    def test_invalid_hex_with_z(self):
        assert is_hex_string("ABCDEFZ12345") == 1

    def test_empty_string(self):
        assert is_hex_string("") == 0


class TestStrToHexList:
    """测试 str_to_hex_list 函数"""

    def test_valid_hex_string(self):
        result = str_to_hex_list("48656c6c6f")
        assert result == [0x48, 0x65, 0x6c, 0x6c, 0x6f]

    def test_valid_hex_string_with_spaces(self):
        result = str_to_hex_list("48 65 6c 6c 6f")
        assert result == [0x48, 0x65, 0x6c, 0x6c, 0x6f]

    def test_odd_length_returns_error(self):
        result = str_to_hex_list("48656c6c6")
        assert result == "ERROR_LENGTH"

    def test_invalid_character_returns_error(self):
        result = str_to_hex_list("48656c6c6G")
        assert result == "ERROR_CHARACTER"


class TestIntToStr:
    """测试 int_to_str 函数"""

    def test_small_number(self):
        result = int_to_str(0x48656c6c6f, 5)
        assert "48" in result
        assert "65" in result

    def test_zero(self):
        result = int_to_str(0, 4)
        assert result == "00 00 00 00"

    def test_max_bytes(self):
        result = int_to_str(0xFFFFFFFF, 4)
        assert "FF" in result


class TestHexListToStr:
    """测试 hex_list_to_str 函数"""

    def test_valid_hex_list(self):
        result = hex_list_to_str([0x48, 0x65, 0x6c, 0x6c, 0x6f])
        assert result == "48656c6c6f"

    def test_empty_list(self):
        result = hex_list_to_str([])
        assert result == ""


class TestStrToInt:
    """测试 str_to_int 函数"""

    def test_valid_hex_string(self):
        result = str_to_int("48656c6c6f")
        assert result == 0x48656c6c6f

    def test_valid_hex_string_with_spaces(self):
        result = str_to_int("48 65 6c 6c 6f")
        assert result == 0x48656c6c6f

    def test_odd_length_returns_none(self):
        result = str_to_int("48656c6c6")
        assert result is None


class TestIntToHexList:
    """测试 int_to_hex_list 函数"""

    def test_small_number(self):
        result = int_to_hex_list(0x48656c6c6f, 5)
        assert result == [0x48, 0x65, 0x6c, 0x6c, 0x6f]

    def test_zero(self):
        result = int_to_hex_list(0, 4)
        assert result == [0x00, 0x00, 0x00, 0x00]

    def test_exact_length(self):
        result = int_to_hex_list(0xABCD, 2)
        assert result == [0xAB, 0xCD]
