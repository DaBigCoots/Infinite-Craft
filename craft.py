import catalog
import database
import client
import requests
import time


def single_request():
    item1 = input("Enter first item: ").lower().strip()
    item2 = input("Enter second item: ").lower().strip()
    if catalog.validate_input(
        item1, item2
    ):  # TODO Sanitize input to string probably using regex. This will ensure proper values sent to api and prevent sql injection. This will also fix a defect in which a user has a leading or trailing spaces
        response = client.send_request(item1, item2)
        if response.status_code == requests.codes.ok:
            jsonResponse = response.json()
            database.update_database(
                client.parse_json(jsonResponse, "result"),
                client.parse_json(jsonResponse, "emoji"),
                client.parse_json(jsonResponse, "isNew"),
                item1,
                item2,
            )
        else:
            print(
                "Request failed. Error: "
                + str(response.status_code)
                + " Try again. If error persists, try a different combination."
            )


def infinite_requests():
    item1_id = 1
    item2_id = 2
    first_discovery_limit = 1000
    while True:
        total_first_discoveries = database.get_item_by_new(True)
        if total_first_discoveries:
            total_first_discoveries = len(total_first_discoveries)
        else:
            total_first_discoveries = 0
        if total_first_discoveries >= first_discovery_limit:
            print("Reached maximum first discovery limit. Stopping request loop")
            break
        item1 = database.get_item_by_id(item1_id)
        item2 = database.get_item_by_id(item2_id)
        if item2 is False:
            item2_id = 1
            item1_id += 1
            continue
        else:
            time.sleep(
                0.4
            )  # wait .2 seconds between each request. Cloudflare banned without limit
            print(
                "Searching: ["
                + str(item1[0])
                + "] "
                + str(item1[1])
                + " + ["
                + str(item2[0])
                + "] "
                + str(item2[1])
            )
            response = client.send_request(item1[1], item2[1])
            if response.status_code == requests.codes.ok:
                jsonResponse = response.json()
                database.update_database(
                    client.parse_json(jsonResponse, "result"),
                    client.parse_json(jsonResponse, "emoji"),
                    client.parse_json(jsonResponse, "isNew"),
                    item1[1],
                    item2[1],
                )
            else:
                print(
                    "Request failed. Error: "
                    + str(response.status_code)
                    + " Try again. If error persists, try a different combination."
                )
            item2_id += 1
