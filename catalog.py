import database


def show_item_details(item):
    if item:
        print("Item ID: " + str(item[0]))
        print("Name: " + str(item[1]))
        print("Emoji: " + str(item[2]))
        print("First Discovery: " + str(item[3]))
        print("Times Encountered: " + str(item[4]))
        print("First Ingredient: " + str(item[5]))
        print("Second Ingredient: " + str(item[6]))
        return item
    else:
        print("Item not found in catalog.")
        return False


def get_first_discoveries(item_list):
    if item_list:
        for item in item_list:
            print("Item ID: " + str(item[0]))
            print("Name: " + str(item[1]))
            print("Emoji: " + str(item[2]))
            print("Times Encountered: " + str(item[4]))
            print("First Ingredient: " + str(item[5]))
            print("Second Ingredient: " + str(item[6]))
        return item_list
    else:
        print("There are no 'First Discoveries'")
        return False


def validate_input(item1, item2):
    # Check if the item is already in the DB and increment the time_encountered
    item1_exists = database.get_item_by_name(item1)
    item2_exists = database.get_item_by_name(item2)
    if item1_exists:
        if item2_exists:
            return True
        else:
            print(
                str(item2).capitalize()
                + " is not an available ingredient in the catalog"
            )
            return False
    else:
        print(
            str(item1).capitalize() + " is not an available ingredient in the catalog"
        )
        return False


# def get_latest_item():
#     connection = sqlite3.connect(database.db_name)
#     cursor = connection.cursor()
#     latest_item = cursor.execute("SELECT MAX(id) FROM item").fetchone()
