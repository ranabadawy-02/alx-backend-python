#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test the GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json):
        """Test that GithubOrgClient.org returns correct payload and calls get_json once"""
        # Arrange: mock get_json return value
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        # Act: create GithubOrgClient instance and call org
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert: org property returns expected payload
        self.assertEqual(result, expected_payload)
        # Assert: get_json called once with correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
