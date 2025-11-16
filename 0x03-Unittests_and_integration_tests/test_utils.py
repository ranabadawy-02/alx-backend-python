#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map and utils.get_json"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns correct values"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test that access_nested_map raises KeyError for missing keys"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(cm.exception.args[0], expected_key)


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



class TestMemoize(unittest.TestCase):
    """Test cases for utils.memoize decorator"""

    def test_memoize(self):
        """Test that a memoized method is called only once"""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_instance = TestClass()

        # Patch 'a_method' of our test instance
        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            # Call the memoized property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            # Check that the result is correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Check that a_method was called only once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()

