#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""

import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient.org"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org property returns the correct payload"""
        # Mock payload
        payload = {"login": org_name}
        mock_get_json.return_value = payload

        # Instantiate GithubOrgClient
        client = GithubOrgClient(org_name)
        result = client.org  # access property

        # Assert get_json called with expected URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        # Assert returned value is as expected
        self.assertEqual(result, payload)


if __name__ == "__main__":
    unittest.main()
