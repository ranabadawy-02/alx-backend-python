#!/usr/bin/env python3
import time
import sqlite3
import functools

# Reuse the decorator from previous tasks
def with_db_connection(func):
    """Decorator that opens a database connection, passes it to the function,
    and closes it automatically afterward."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


# Global cache dictionary
query_cache = {}


# New decorator to cache query results
def cache_query(func):
    """Decorator that caches database query results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query in query_cache:
            print("Using cached result for query:", query)
            return query_cache[query]
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        print("Caching result for query:", query)
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
