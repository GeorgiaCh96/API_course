from app.calculations import *
import pytest

@pytest.mark.parametrize("num1, num2, expected", 
                         [
                             (3, 2, 5),
                             (7, 1, 8),
                             (12, 4, 16)
                         ])
def test_add(num1, num2, expected):
    print(" testing add function")
    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(5,2) ==3

