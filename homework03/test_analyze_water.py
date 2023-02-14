from analyze_water import calculate_turbidity, calculate_minimum_left
import pytest

def test_calculate_turbidity():
    assert calculate_turbidity(1.2343,0.999) == 1.2343*0.999

def test_calculate_minimum_left():
    assert calculate_minimum_left(.999) == 0
    assert calculate_minimum_left(1.23) == 11
