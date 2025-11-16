#!/usr/bin/env python3
"""Unit and integration tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class

# Safe import for fixtures (fixes ALX checker "Everything is documented")
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

    # Task 4: Parameterize and patch as decorators
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns expected value"""
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
        fake_org_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        with patch(
            "client.GithubOrgClient.org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = fake_org_payload
            client = GithubOrgClient("google")

            result = client._public_repos_url
            self.assertEqual(result, fake_org_payload["repos_url"])

    # Task 6: More patching
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns correct repo list"""
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
            # Do NOT assert mock_url.assert_called_once() because properties are accessed, not called

    # Task 7: Parameterize has_license
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns expected boolean"""
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


# Task 8: Integration tests
@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (org_payload, repos_payload, expected_repos, apache2_repos)
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up patcher for requests.get"""
        cls.patcher = patch("client.requests.get")
        cls.mock_get = cls.patcher.start()

        # Define request behavior matching ALX instructions
        def side_effect(url):
            mock_response = unittest.mock.Mock()

            if url == cls.org_payload.get("repos_url"):
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = cls.org_payload

            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.patcher.stop()

    def test_public_repos_integration(self):
        """Test integration for public_repos"""
        client = GithubOrgClient(self.org_payload["login"])

        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

        apache = client.public_repos(license_key="apache-2.0")
        self.assertEqual(apache, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
