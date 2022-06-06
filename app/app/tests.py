"""
Sample Tests
"""

from django.test import SimpleTestCase

from app import calc


class CalcTests(SimpleTestCase):
    """Test the calc module."""
    def test_add_numbers(self):
        """TEST ADDING NUMBERS TOGETHER"""
        res = calc.add(5,6)

        self.assertEqual(res,11)