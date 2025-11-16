#!/usr/bin/env python3
"""GithubOrgClient module"""

import requests
from typing import List, Dict


def get_json(url: str) -> Dict:
    """Return the JSON response from a URL"""
    response = requests.get(url)
    return response.json()


class GithubOrgClient:
    """Client for GitHub organization"""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org: str):
        self._org = org

    @property
    def org(self) -> Dict:
        """Return the organization metadata"""
        return get_json(self.ORG_URL.format(org=self._org))

    @property
    def _public_repos_url(self) -> str:
        """Return repos_url from org"""
        return self.org.get("repos_url")

    def public_repos(self, license: str = None) -> List[str]:
        """
        Return list of public repo names.
        If license is provided, filter by that license key.
        """
        repos = get_json(self._public_repos_url)
        repo_names = []

        for repo in repos:
            if license is None:
                repo_names.append(repo["name"])
            else:
                if self.has_license(repo, license):
                    repo_names.append(repo["name"])

        return repo_names

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Return True if the repo has the specified license"""
        try:
            return repo["license"]["key"] == license_key
        except Exception:
            return False
