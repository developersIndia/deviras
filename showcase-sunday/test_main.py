import unittest
import datetime
from main import is_second_sunday
import unittest.mock


# Unit test class
class TestIsSecondSunday(unittest.TestCase):
    def test_second_sunday(self):
        # Define test cases as a list of tuples containing (input_date, expected_result)
        test_cases = [
            (datetime.date(2023, 12, 10), True),
            (datetime.date(2024, 1, 14), True),
            (datetime.date(2024, 2, 11), True),
        ]

        for input_date, expected_result in test_cases:
            with unittest.mock.patch("datetime.date") as mock_date:
                mock_date.today.return_value = input_date
                self.assertEqual(is_second_sunday(), expected_result)

    def test_not_second_sunday(self):
        # Define test cases as a list of tuples containing (input_date, expected_result)
        test_cases = [
            (datetime.date(2023, 12, 12), False),
            (datetime.date(2023, 12, 5), False),
            (datetime.date(2023, 12, 19), False),
        ]

        for input_date, expected_result in test_cases:
            with unittest.mock.patch('datetime.date') as mock_date:
                mock_date.today.return_value = input_date
                self.assertEqual(is_second_sunday(), expected_result)


if __name__ == "__main__":
    unittest.main()
