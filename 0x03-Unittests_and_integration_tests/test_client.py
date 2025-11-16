#!/usr/bin/env python3
""" Test module for client.py """
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """ TestGithubOrgClient class """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org, mock_get_json):
        """ test org method """
        mock_get_json.return_value = {"payload": True}
        client = GithubOrgClient(org)
        self.assertEqual(client.org, {"payload": True})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org}"
        )

    def test_public_repos_url(self):
        """ test _public_repos_url """
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock,
            return_value={"repos_url": "URL"}
        ):
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, "URL")

    @patch('client.get_json')
    def test_public_repos(self, mock_json):
        """ test public_repos """
        mock_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value="URL"
        ) as mock_url:
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_json.assert_called_once_with("URL")
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False),
    ])
    def test_has_license(self, repo, key, expected):
        """ test has_license """
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
    """ Integration tests """

    @classmethod
    def setUpClass(cls):
        """ Set up class """
        cls.get_patcher = patch('requests.get')

        mock = cls.get_patcher.start()

        def side_effect(url):
            mock_resp = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_resp.json.return_value = cls.org_payload
            elif url == "https://api.github.com/orgs/google/repos":
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = {}
            return mock_resp

        mock.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """ Tear down class """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """ test public_repos (integration) """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """ test public_repos with license filter """
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
