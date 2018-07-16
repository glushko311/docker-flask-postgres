from unittest import TestCase

class TestSuit1(TestCase):
    def test_single(self):
        return self.assertEqual(1, 1)
		
    def test_two(self):
        return self.assertEqual(2, 2)

    def test_two(self):
        return self.assertEqual(3, 3)

if __name__ == "__main__":
    TestSuit1()