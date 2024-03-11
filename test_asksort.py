import unittest
from unittest.mock import patch
from asksort import Item, ComparisonMemo


class TestItemComparison(unittest.TestCase):
    def setUp(self):
        self.comparison_memo = ComparisonMemo()

    @patch("builtins.input", side_effect=["y", "y"])
    def test_transitivity(self, mock_input):
        item1 = Item("Apple", self.comparison_memo)
        item2 = Item("Banana", self.comparison_memo)
        item3 = Item("Carrot", self.comparison_memo)

        self.assertTrue(item1 > item2)  # User indicates Apple > Banana
        self.assertTrue(item2 > item3)  # User indicates Banana > Carrot

        # Check transitivity inference (Apple > Carrot) without further user input
        comparison_result = self.comparison_memo.get_comparison("Apple", "Carrot")

        self.assertIsNotNone(
            comparison_result,
            "Transitivity failed: No inference made for Apple > Carrot",
        )
        self.assertTrue(
            comparison_result,
            "Transitivity failed: Incorrect comparison result for Apple > Carrot",
        )


if __name__ == "__main__":
    unittest.main()
