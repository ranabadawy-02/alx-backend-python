#!/usr/bin/python3
import mysql.connector


def stream_users():
    """Generator that streams rows one by one from the user_data table"""
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_mysql_password",  # ← replace with your real password
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        # Yield one row at a time
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection:
            connection.close()
