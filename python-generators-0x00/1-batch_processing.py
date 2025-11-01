#!/usr/bin/python3
import mysql.connector


def stream_users_in_batches(batch_size):
    """Generator that fetches rows from user_data table in batches."""
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_mysql_password",  # ← replace with your actual password
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        batch = []
        for row in cursor:
            batch.append(row)
            # When batch reaches desired size, yield it and reset
            if len(batch) == batch_size:
                yield batch
                batch = []

        # Yield remaining rows if they don’t fill the batch
        if batch:
            yield batch

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """Process each batch and yield users over age 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
