import unittest

from jupyter.user import User


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User()
        return super().setUp()
    
    def test_user_should_subscribe_strategy(self):
        obj = object()
        self.user.add_strategy(obj)

        self.assertEqual(len(self.user.strategies), 1)
        self.assertEqual(self.user.strategies[0], obj)