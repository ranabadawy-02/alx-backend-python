#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @patch("client.get_json")
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the expected value"""

        # Setup mock return value
        mock_get_json.return_value = {"login": org_name}

        # Instantiate GithubOrgClient
        client = GithubOrgClient(org_name)

        # Call the method
        result = client.org()

        # Assertions
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, {"login": org_name})


if __name__ == "__main__":
    unittest.main()
