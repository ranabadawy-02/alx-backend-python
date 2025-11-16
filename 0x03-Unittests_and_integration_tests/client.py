#!/usr/bin/env python3
"""Stub client.py for GithubOrgClient"""
from typing import Any, List
import utils  # make sure utils.py exists

class GithubOrgClient:
    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org: str) -> None:
        self.org_name = org

    @property
    def org(self) -> dict:
        """Return mocked org payload"""
        return utils.get_json(self.ORG_URL.format(org=self.org_name))

    @property
    def _public_repos_url(self) -> str:
        return self.org.get("repos_url", "")

    def public_repos(self, license: str = None) -> List[str]:
        repos = utils.get_json(self._public_repos_url)
        names = [r["name"] for r in repos]
        if license:
            names = [r["name"] for r in repos if r.get("license", {}).get("key") == license]
        return names

    @staticmethod
    def has_license(repo: dict, license_key: str) -> bool:
        return repo.get("license", {}).get("key") == license_key
