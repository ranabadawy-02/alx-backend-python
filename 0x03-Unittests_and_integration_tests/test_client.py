#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @patch("client.get_json")
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    def test_org(self, mock_get_json, org_name):
        """Test that GithubOrgClient.org returns the correct value"""
        mock_get_json.return_value = {"key": "value"}

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, {"key": "value"})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
