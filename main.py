import requests
import sqlite3

db_name = "infiniteItems.db"
default_items = ("water", "fire", "wind", "earth")


def create_db_connection():
    # Connect to the DB
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    # Create table if it doesn't exist
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS item (id INTEGER, name TEXT NOT NULL, emoji TEXT NOT NULL, new BOOLEAN NOT NULL, times_encountered INTEGER NOT NULL, first_ingredient TEXT NOT NULL, second_ingredient TEXT NOT NULL)"
    )
    # get the current number of items in table
    newId = cursor.execute("SELECT MAX(id) FROM item").fetchone()
    # if the table is empty, add the default items
    if newId[0] is None:
        count = 0
        for name in default_items:
            count += 1
            cursor.execute(
                "INSERT INTO item VALUES (?, ?, '', 0, 0, '', '')", (count, name)
            )
        connection.commit()
        connection.close()


def update_database(name, emoji, isNew, first, second):
    # Connect to the DB
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    name = name.lower()
    # Check if the item is already in the DB and increment the time_encountered
    try:
        known = cursor.execute(
            "SELECT times_encountered FROM item WHERE name = ?", (name,)
        ).fetchone()
        if known[0] > 0:
            count = int(known[0]) + 1
            cursor.execute(
                "UPDATE item SET times_encountered = ? WHERE name = ?",
                (count, name),
            )
        print(
            "You previously encountered "
            + name
            + " "
            + emoji
            + "  "
            + str(known[0])
            + " times."
        )
    # Update DB with new item
    except:
        # get the current number of items and add new item with new id
        newId = cursor.execute("SELECT MAX(id) FROM item").fetchone()
        newId = int(newId[0] + 1)
        print("Discovered " + name + " " + emoji)
        cursor.execute(
            "INSERT INTO item VALUES (?,?, ?, ?, 1, ?, ?)",
            (newId, name, emoji, isNew, first, second),
        )
    # List all items in the DB and commit the changes to DB and close the connection
    finally:
        item_list = cursor.execute("SELECT id, name, emoji FROM item").fetchall()
        connection.commit()
        connection.close()
        # print each item and emoji on a new line
        for item in item_list:
            print(item[0], item[1])


def send_request(item1, item2):
    payload = {"first": item1, "second": item2}
    url = "https://neal.fun/api/infinite-craft/pair"
    headers = {"Referer": "https://neal.fun/infinite-craft/"}
    x = requests.get(url, headers=headers, params=payload)
    return x


def validate_input(item1, item2):
    # Connect to the DB
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    # Check if the item is already in the DB and increment the time_encountered
    item1_exists = cursor.execute(
        "SELECT 1 FROM item WHERE name = ?", (item1,)
    ).fetchone()
    item2_exists = cursor.execute(
        "SELECT 1 FROM item WHERE name = ?", (item2,)
    ).fetchone()
    if item1_exists:
        if item2_exists:
            return 1
        else:
            print(
                str(item2).capitalize()
                + " is not an available ingredient in the catalog"
            )
            return 0
    else:
        print(
            str(item1).capitalize() + " is not an available ingredient in the catalog"
        )
        return 0


def main():
    create_db_connection()
    while True:
        item1 = input("Enter first item: ").lower().strip()
        item2 = input("Enter second item: ").lower().strip()
        if validate_input(
            item1, item2
        ):  # TODO Sanitize input to string probably using regex. This will ensure proper values sent to api and prevent sql injection. This will also fix a defect in which a user has a leading or trailing spaces
            jsonResponse = send_request(item1, item2).json()
            update_database(
                jsonResponse["result"],
                jsonResponse["emoji"],
                jsonResponse["isNew"],
                item1,
                item2,
            )


if __name__ == "__main__":
    main()
