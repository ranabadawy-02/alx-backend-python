#!/usr/bin/env python3
import asyncio
import aiosqlite


# Asynchronous function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


# Asynchronous function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()


# Function to fetch both concurrently
async def fetch_concurrently():
    results_all, results_older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All users:", results_all)
    print("Users older than 40:", results_older)


# Run the concurrent fetch
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
