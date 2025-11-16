#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url property"""

        # Known payload to mock org property
        fake_org_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        # Patch the 'org' property
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = fake_org_payload

            client = GithubOrgClient("google")
            # Access the property
            result = client._public_repos_url

            # Assert the property returns the correct repos_url
            self.assertEqual(result, fake_org_payload["repos_url"])


if __name__ == "__main__":
    unittest.main()
