#!/usr/bin/env python3
"""Stub utils.py with memoize, access_nested_map, get_json"""
from typing import Any, Dict, Tuple

def access_nested_map(nested_map: Dict, path: Tuple[str, ...]) -> Any:
    for key in path:
        nested_map = nested_map[key]
    return nested_map

def get_json(url: str) -> dict:
    """Stub that should be mocked in tests"""
    return {}

def memoize(fn):
    """Simple memoize decorator"""
    attr_name = "_memoized_" + fn.__name__

    @property
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return wrapper
