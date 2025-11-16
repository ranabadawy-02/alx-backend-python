#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient.org property"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("utils.get_json")  # <-- patch the exact import used in client.py
    def test_org(self, org_name, mock_get_json):
        """Test that org returns the correct payload"""
        mock_payload = {"login": org_name}
        mock_get_json.return_value = mock_payload

        client = GithubOrgClient(org_name)
        result = client.org  # access property

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, mock_payload)


if __name__ == "__main__":
    unittest.main()
