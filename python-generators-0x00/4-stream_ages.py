#!/usr/bin/python3
import seed


def stream_user_ages():
    """Generator that yields user ages one by one"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row["age"]
    connection.close()


def calculate_average_age():
    """Calculate average age using the generator (no full data load)"""
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average = total / count
        print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()
