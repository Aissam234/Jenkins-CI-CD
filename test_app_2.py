"""
Test file 2 for Flask application
This is a simple test file to demonstrate parallel testing in Jenkins
"""

def test_example():
    """Test basic arithmetic"""
    assert 4 * 5 == 20


def test_addition():
    """Test addition operation"""
    assert 10 + 5 == 15


def test_subtraction():
    """Test subtraction operation"""
    assert 20 - 8 == 12


def test_string_operations():
    """Test string concatenation"""
    result = "Hello" + " " + "World"
    assert result == "Hello World"


def test_list_operations():
    """Test list operations"""
    my_list = [1, 2, 3]
    my_list.append(4)
    assert len(my_list) == 4
    assert my_list[-1] == 4
