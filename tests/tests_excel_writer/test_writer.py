from parser_logfile.excel_writer import writer
import pytest

list_test_writer_negative = [
    ({'a': 'A', 'b': 'B'}, False),
    ({'input_file': 'something', 'b': 'B'}, False),
    ()
]


#@pytest.mark.parametrize("dict, expected_result", list_test_writer_negative):