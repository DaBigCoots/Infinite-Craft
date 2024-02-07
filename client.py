import requests


def send_request(item1, item2):
    payload = {"first": item1, "second": item2}
    url = "https://neal.fun/api/infinite-craft/pair"
    headers = {"Referer": "https://neal.fun/infinite-craft/"}
    x = requests.get(url, headers=headers, params=payload)
    return x


def parse_json(json_body, key):
    value = ""
    try:
        value = json_body[key]
    except KeyError:
        print("Missing '" + key + "' key in JSON data")
    finally:
        return value
