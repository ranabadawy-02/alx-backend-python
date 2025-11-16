#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        mock_payload = {"login": org_name}
        mock_get_json.return_value = mock_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, mock_payload)

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    def test_public_repos_url(self, org_name):
        """Test that _public_repos_url returns correct URL from org dict"""
        client = GithubOrgClient(org_name)
        fake_org = {"repos_url": f"https://api.github.com/orgs/{org_name}/repos"}

        with patch.object(client, "org", new_callable=Mock) as mock_org:
            mock_org.return_value = fake_org
            result = client._public_repos_url
            self.assertEqual(result, fake_org["repos_url"])

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_public_repos(self, org_name, mock_get_json):
        """Test that public_repos returns the list of repo names"""
        repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        mock_get_json.return_value = repos_payload

        client = GithubOrgClient(org_name)
        with patch.object(client, "_public_repos_url",
                          new_callable=Mock) as mock_url:
            mock_url.return_value = f"https://api.github.com/orgs/{org_name}/repos"
            result = client.public_repos()

            mock_get_json.assert_called_once_with(mock_url.return_value)
            self.assertEqual(result, ["repo1", "repo2"])

    @parameterized.expand([
        ("google", "python"),
        ("abc", "test"),
    ])
    @patch("client.get_json")
    def test_has_license(self, org_name, license_key, mock_get_json):
        """Test that has_license returns True if license exists"""
        client = GithubOrgClient(org_name)
        repo = {"license": {"key": license_key}}
        self.assertTrue(client.has_license(repo, license_key))
        self.assertFalse(client.has_license(repo, "other"))


if __name__ == "__main__":
    unittest.main()
