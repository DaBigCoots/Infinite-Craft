import sqlite3
import database
import catalog
import craft


def get_game_stats():
    connection = sqlite3.connect(database.db_name)
    cursor = connection.cursor()
    total_items = cursor.execute("SELECT MAX(id) FROM item").fetchone()
    total_requests = cursor.execute(
        "SELECT SUM(times_encountered) FROM item"
    ).fetchone()
    item = cursor.execute("SELECT name, MAX(times_encountered) FROM item").fetchone()
    total_first_discoveries = cursor.execute(
        "SELECT name FROM item WHERE new = true"
    ).fetchall()
    print("Total items discovered: " + str(total_items[0]))
    print("Total combination requests made: " + str(total_requests[0]))
    print("Total first discoveries: " + str(len(total_first_discoveries)))
    print("Most created item: " + item[0] + " Times created: " + str(item[1]))
    connection.close()


def main():
    database.create_db_connection()
    while True:
        print()
        print("*************************")
        print("Please make a selection:")
        print("1: List First Discoveries")
        print("2: Create combination")
        print("3: Search item catalog")
        print("4: Game statistics")
        print("*************************")
        selection = input()
        if selection == "1":
            catalog.get_first_discoveries(database.get_item_by_new(True))
            continue
        if selection == "2":
            craft.single_request()
            continue
        if selection == "3":
            catalog.show_item_details(database.get_item_by_name(input("Search: ")))
            continue
        if selection == "4":
            get_game_stats()
            continue
        if selection == "↑↑↓↓←→←→🅱️🅰️":
            craft.infinite_requests()
            continue
        else:
            print("Invalid selection")
            continue


if __name__ == "__main__":
    main()
