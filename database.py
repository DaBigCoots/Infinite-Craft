import sqlite3
import catalog

db_name = "infiniteItems.db"


def create_db_connection():
    # Connect to the DB
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    # Create table if it doesn't exist
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS item (id INTEGER UNIQUE, name TEXT NOT NULL, emoji TEXT, new TEXT, times_encountered INTEGER NOT NULL, first_ingredient TEXT NOT NULL, second_ingredient TEXT NOT NULL)"
    )
    # get the current number of items in table
    new_id = cursor.execute("SELECT MAX(id) FROM item").fetchone()
    # if the table is empty, add the default items
    if new_id[0] is None:
        default_items = ("water", "fire", "wind", "earth")
        default_emojis = "💧,🔥,💨,"
        count = 0
        for name in default_items:
            count += 1
            cursor.execute(
                "INSERT INTO item VALUES (?, ?, '', 0, 0, '', '')", (count, name)
            )
    connection.commit()
    connection.close()


def get_item_by_name(name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    name = name.lower().strip()
    item_details = cursor.execute(
        "SELECT * FROM item WHERE name = ?",
        (name,),
    ).fetchone()
    connection.close()
    if item_details:
        return item_details
    else:
        return False


def get_item_by_id(id):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    item_details = cursor.execute(
        "SELECT * FROM item WHERE id = ?",
        (id,),
    ).fetchone()
    connection.close()
    if item_details:
        return item_details
    else:
        return False


def get_item_by_new(isNew):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    item_details = cursor.execute(
        "SELECT * FROM item WHERE new = ?",
        (isNew,),
    ).fetchall()
    connection.close()
    if item_details:
        return item_details
    else:
        return 0


def del_row(id):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    item_id = int(id)
    item = get_item_by_id(item_id)
    cursor.execute("DELETE FROM item WHERE id = ?", (item_id,))
    connection.commit()
    connection.close()
    if item:
        print("Successfully deleted row [" + id + "]")
        return item
    else:
        print("Failed to deleted row [" + id + "] Does it exist?")
        return False


def update_database(name, emoji, isNew, first, second):
    # Connect to the DB
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    name = name.lower()
    # Check if the item is already in the DB and increment the time_encountered
    try:
        item = get_item_by_name(name)
        if item:
            count = int(item[4]) + 1
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
            + str(item[4])
            + " times."
        )
    # Update DB with new item
    except:
        # get the current number of items and add new item with new id
        new_id = cursor.execute("SELECT MAX(id) FROM item").fetchone()
        new_id = int(new_id[0] + 1)
        print("Discovered item " + str(new_id) + ": " + name + " " + emoji)
        cursor.execute(
            "INSERT INTO item VALUES (?,?, ?, ?, 1, ?, ?)",
            (new_id, name, emoji, isNew, first, second),
        )
    # List all items in the DB and commit the changes to DB and close the connection
    finally:
        connection.commit()
        connection.close()
