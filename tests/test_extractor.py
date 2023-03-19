import unittest

from src.extractor import CSVExtractor, StudentsBySchoolGenderExtractor


class TestCSVExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = CSVExtractor()

    def test_num_str_to_int(self):
        self.assertEqual(self.extractor.num_str_to_int('10'), 10)
        self.assertEqual(self.extractor.num_str_to_int('-'), 0)

    def test_extract_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            self.extractor.extract([])


class TestStudentsBySchoolGenderExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = StudentsBySchoolGenderExtractor()

    def test_extract(self):
        row = [
            '1', 'School 1', 'Day', 'Bachelors',
            '10', '5', '5', '3', '2', '2', '1', '1', '1', '1', '0', '0', '0',
            '0', '0', '0', '0', '0', '0', 'City 1', 'Public'
        ]
        expected_output = [
            1, 'School 1', 'Day', 'Bachelors',
            10, 5, 5, 3, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'City 1', 'Public'
        ]
        self.assertEqual(self.extractor.extract(row), expected_output)
