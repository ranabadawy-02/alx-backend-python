#!/usr/bin/env python3
"""Unit tests for utils.get_json"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import get_json


class TestGetJson(unittest.TestCase):
    """Test cases for utils.get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test that get_json returns the expected payload"""
        # Configure the mock to return a response with .json() method
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call get_json
        result = get_json(test_url)

        # Check that requests.get was called exactly once with test_url
        mock_get.assert_called_once_with(test_url)

        # Check that get_json returned the expected payload
        self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()


