#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


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

    def test_access_nested_map_exception(self):
        """Test access_nested_map raises KeyError properly"""
        cases = [
            ({}, ("a",)),
            ({"a": 1}, ("a", "b")),
        ]

        for nested_map, path in cases:
            with self.assertRaises(KeyError) as error:
                access_nested_map(nested_map, path)

            self.assertEqual(error.exception.args[0], path[-1])
