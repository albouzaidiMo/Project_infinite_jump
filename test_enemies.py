from enemies import *
import pytest

def test_random_position_in_platform_with_width():
    platform_sol = [ 0 , 800 , 20]
    platform_haute = [ 250 , 680 , 70]
    
    assert random_position_in_platform_with_width( platform_sol , 40 , 10) [1] == 60
    assert random_position_in_platform_with_width( platform_sol , 40 , 10) [0] in list(range(791))
    assert random_position_in_platform_with_width( platform_sol , 20 , 100) [0] in list(range(701))
    assert random_position_in_platform_with_width( platform_haute , 30 , 10 ) [1] == 100
    assert random_position_in_platform_with_width( platform_haute , 20 , 10) [0] in list(range(250,671))
    assert random_position_in_platform_with_width( platform_haute , 20 , 250) [0] in list(range(250,461))

