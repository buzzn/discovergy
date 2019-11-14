import unittest
from discovergy.discovergy import Discovergy


class DiscovergyTestCase(unittest.TestCase):
    """ Unit tests for class Discovergy """

    def setUp(self):
        self.discovergy = Discovergy("TestClient")

    def tearDown(self):
        self.discovergy.dispose()


if __name__ == "__main__":
    unittest.main()
