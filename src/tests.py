import os
import flaskr
import unittest
import tempfile
import requests
 

class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        return 0

    def tearDown(self):
        return 0

    def test_hello_world(self):
        r = requests.get("localhost:5000")


if __name__ == '__main__':
    unittest.main()
