import unittest
from unittest.mock import Mock, ANY

from src.transformer import StudentsByGenderTransformer


class TestStudentsByGenderTransformer(unittest.TestCase):
    def setUp(self):
        self.mock_raw_dao = Mock()
        self.mock_dao = Mock()
        self.transformer = StudentsByGenderTransformer(self.mock_raw_dao, self.mock_dao)

    def test_transform(self):
        school_year = 2022
        self.mock_raw_dao.select_students_by_gender.return_value = {
            'school_year': school_year,
            'total': 1000,
            'male': 500,
            'female': 500
        }

        self.transformer.transform(school_year)

        expected_data = (2022, 1000, ANY, 500, ANY, 500, ANY)
        self.mock_dao.insert_students_by_gender.assert_called_once_with(expected_data)

    def test_transform_no_data(self):
        school_year = 2022
        self.mock_raw_dao.select_students_by_gender.side_effect = KeyError('no data')

        self.transformer.transform(school_year)

        self.assertFalse(self.mock_dao.insert_students_by_gender.called)


if __name__ == '__main__':
    unittest.main()
