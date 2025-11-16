#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org method returns correct value and calls get_json once"""
        # Arrange: set mock return value
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        # Act: create client and call org
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert: org returns what get_json returned
        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
