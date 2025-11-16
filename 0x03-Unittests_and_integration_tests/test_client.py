#!/usr/bin/env python3
"""Test GithubOrgClient"""
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test the GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, name, mock_get_json):
        """Test org returns correct value"""
        mock_get_json.return_value = {"payload": True}
        client = GithubOrgClient(name)
        self.assertEqual(client.org, {"payload": True})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{name}"
        )

    def test_public_repos_url(self):
        """Test _public_repos_url"""
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock,
            return_value={"repos_url": "url"}
        ):
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, "url")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos"""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value="url"
        ) as mock_url:
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("url")
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_key"}}, "my_key", True),
        ({"license": {"key": "other"}}, "my_key", False)
    ])
    def test_has_license(self, repo, key, expected):
        """Test has_license"""
        self.assertEqual(
            GithubOrgClient.has_license(repo, key),
            expected
        )


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class"""

    @classmethod
    def setUpClass(cls):
        """Mock requests.get"""

        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            response = Mock()
            if url == "https://api.github.com/orgs/google":
                response.json.return_value = cls.org_payload
            elif url == "https://api.github.com/orgs/google/repos":
                response.json.return_value = cls.repos_payload
            else:
                response.json.return_value = {}
            return response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos integration"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filter"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
