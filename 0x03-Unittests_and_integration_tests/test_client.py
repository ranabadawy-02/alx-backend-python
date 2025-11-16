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
    @patch("utils.get_json")  # patch the import used inside client.py
    def test_org(self, org_name, mock_get_json):
        """Test that org returns the correct payload"""
        # Mock return value
        mock_payload = {"login": org_name}
        mock_get_json.return_value = mock_payload

        # Instantiate client and access property
        client = GithubOrgClient(org_name)
        result = client.org  # access as property

        # Ensure get_json called once with correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        # Ensure result matches mock payload
        self.assertEqual(result, mock_payload)


if __name__ == "__main__":
    unittest.main()
