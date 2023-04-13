import pytest
import os
from parser_logfile.gui_entry_point import Root

test_root = Root()


list_for_test_check_valid_input_negative = [
    ("", True, False),
    ("cow.png", True, False),
    ("cow.log", True, False),
    ("https:\ww.zoo.com\cow.log", True, False),
    ("unexisting_file.log", True, False),
]


@pytest.mark.parametrize("text, input_file, expected_result", list_for_test_check_valid_input_negative)
def test_check_valid_input_negative(text, input_file, expected_result):
    assert test_root.check_valid(text, input_file=input_file) == expected_result


list_for_test_check_valid_input_positive = [
    (os.getcwd() + "/existing_file.log", True, True),
]


@pytest.mark.parametrize("text, input_file, expected_result", list_for_test_check_valid_input_positive)
def test_check_valid_input_positive(text, input_file, expected_result):
    assert test_root.check_valid(text, input_file=input_file) == expected_result


list_for_test_check_valid_output_negative = [
    ("", True, False),
    ("unexisting_dir", True, False),
    ("some_file.txt", True, False),
    (os.getcwd() + "/existing_file.log", True, False),
]


@pytest.mark.parametrize("text, output_dir, expected_result", list_for_test_check_valid_output_negative)
def test_check_valid_output_negative(text, output_dir, expected_result):
    assert test_root.check_valid(text, output_dir=output_dir) == expected_result


list_for_test_check_valid_output_positive = [
    (os.getcwd(), True, True),
    ("/", True, True),  # only UNIX maybe
]


@pytest.mark.parametrize("text, output_dir, expected_result", list_for_test_check_valid_output_positive)
def test_check_valid_output_positive(text, output_dir, expected_result):
    assert test_root.check_valid(text, output_dir=output_dir) == expected_result
