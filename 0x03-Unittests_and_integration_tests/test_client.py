#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    # Task 4: Parameterize and patch as decorators
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

    # Task 5: Mocking a property
    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url property"""

        # Known payload to mock org property
        fake_org_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        # Patch the 'org' property as a context manager
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = fake_org_payload

            client = GithubOrgClient("google")
            # Access the property
            result = client._public_repos_url

            # Assert the property returns the correct repos_url
            self.assertEqual(result, fake_org_payload["repos_url"])


if __name__ == "__main__":
    unittest.main()
