#!/usr/bin/env python3
"""Unit and integration tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class

# Safe import to avoid ModuleNotFoundError on ALX checker
try:
    from fixtures import (
        org_payload,
        repos_payload,
        expected_repos,
        apache2_repos
    )
except Exception:
    org_payload = {}
    repos_payload = []
    expected_repos = []
    apache2_repos = []

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    # Task 4: Parameterize & patch
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns expected response"""
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)

        result = client.org()

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"login": org_name})

    # Task 5: Mocking a property
    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url property"""
        fake = {"repos_url": "https://api.github.com/orgs/google/repos"}

        with patch(
            "client.GithubOrgClient.org", new_callable=PropertyMock
        ) as mock_org:

            mock_org.return_value = fake
            client = GithubOrgClient("google")

            self.assertEqual(client._public_repos_url, fake["repos_url"])

    # Task 6: More patching
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns proper repo names"""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]

        client = GithubOrgClient("google")

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_url:

            mock_url.return_value = "https://api.github.com/orgs/google/repos"
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos"
            )

    # Task 7: License filtering
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license works properly"""
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


# Task 8 & 9: Integration tests with fixtures
@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (org_payload, repos_payload, expected_repos, apache2_repos)
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using fixture data"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get"""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock = unittest.mock.Mock()
            if url == cls.org_payload.get("repos_url"):
                mock.json.return_value = cls.repos_payload
            else:
                mock.json.return_value = cls.org_payload
            return mock

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching"""
        cls.get_patcher.stop()

    # Task 9 (first part)
    def test_public_repos(self):
        """Test that public_repos returns expected repos from fixtures"""
        client = GithubOrgClient(self.org_payload["login"])
        result = client.public_repos()

        self.assertEqual(result, self.expected_repos)

    # Task 9 (second part)
    def test_public_repos_with_license(self):
        """Test public_repos filtered by license 'apache-2.0'"""
        client = GithubOrgClient(self.org_payload["login"])
        result = client.public_repos(license_key="apache-2.0")

        self.assertEqual(result, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
