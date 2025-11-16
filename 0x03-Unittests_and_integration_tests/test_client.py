#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        Args:
            org_name: The organization name to test
            mock_get_json: Mocked get_json function
        """
        # Setup the expected return value
        expected_response = {"login": org_name, "id": 12345}
        mock_get_json.return_value = expected_response
        # Create instance and call org method
        client = GithubOrgClient(org_name)
        result = client.org
        # Verify get_json was called once with correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        # Verify the result matches expected response
        self.assertEqual(result, expected_response)

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns the expected URL
        based on the mocked org payload
        """
        # Known payload with repos_url
        known_payload = {
            "login": "google",
            "id": 1342004,
            "repos_url": "https://api.github.com/orgs/google/repos"
        }
        # Use patch as context manager to mock the org property
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock,
            return_value=known_payload
        ) as mock_org:
            # Create client instance
            client = GithubOrgClient("google")
            # Access _public_repos_url property
            result = client._public_repos_url
            # Verify the result matches the repos_url from payload
            self.assertEqual(result, known_payload["repos_url"])
            # Verify org property was accessed
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the expected list of repos
        Args:
            mock_get_json: Mocked get_json function
        """
        # Payload that get_json will return (list of repos)
        test_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}},
        ]
        # Mock get_json to return our test payload
        mock_get_json.return_value = test_payload
        # Use context manager to mock _public_repos_url property
        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/google/repos"
        ) as mock_public_repos_url:
            # Create client instance
            client = GithubOrgClient("google")
            # Call public_repos method
            result = client.public_repos()
            # Expected list of repo names
            expected_repos = ["repo1", "repo2", "repo3"]
            # Verify the result matches expected repo names
            self.assertEqual(result, expected_repos)
            # Verify _public_repos_url property was accessed once
            mock_public_repos_url.assert_called_once()
            # Verify get_json was called once with the mocked URL
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license correctly identifies if a repo has a license

        Args:
            repo: Repository dictionary with license information
            license_key: License key to check for
            expected: Expected boolean result
        """
        # Create client instance
        client = GithubOrgClient("google")
        # Call has_license static method
        result = client.has_license(repo, license_key)
        # Verify the result matches expected value
        self.assertEqual(result, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient class"""

    @classmethod
    def setUpClass(cls):
        """
        Set up class fixtures before running tests
        Mock requests.get to return example payloads from fixtures
        """
        # Define the side_effect function for requests.get
        def side_effect(url):
            """
            Side effect function to return appropriate payload based on URL
            Args:
                url: The URL being requested
            Returns:
                Mock response object with json() method
            """
            # Mock response class
            class MockResponse:
                def __init__(self, json_data):
                    self.json_data = json_data

                def json(self):
                    return self.json_data
            # Check which URL is being requested and return appropriate payload
            if url == "https://api.github.com/orgs/google":
                return MockResponse(cls.org_payload)
            elif url == "https://api.github.com/orgs/google/repos":
                return MockResponse(cls.repos_payload)
            return MockResponse({})
        # Start patcher for requests.get
        cls.get_patcher = patch('requests.get', side_effect=side_effect)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        Tear down class fixtures after running tests
        Stop the patcher for requests.get
        """
        cls.get_patcher.stop()


if __name__ == "__main__":
    unittest.main()
