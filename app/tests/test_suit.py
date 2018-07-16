from unittest import TestLoader, TestSuite, TextTestRunner

from .main_test import TestSuit1


if __name__ == '__main__':
    loader = TestLoader()
    suit = TestSuite((
        loader.loadTestsFromTestCase(TestSuit1),
    ))

    runner = TextTestRunner(verbosity=2)
    runner.run(suit)
