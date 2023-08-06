#  Copyright (c) 2020-2021 ETH Zurich, SIS ID and HVL D-ITET
#
"""
Tests for the validation methods by utils
"""
import pytest
from hvl_ccb.utils.validation import (
    validate_number,
    validate_bool,
)


def test_validate_number():
    assert validate_number("Test", 1, None, int) is None
    with pytest.raises(ValueError):
        validate_number("Test", -1, (0, 10), int)


def test_validate_bool():
    with pytest.raises(TypeError):
        validate_bool("Test", "True")
    assert validate_bool("Test", True) is None
