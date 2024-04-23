from types import NoneType
import requests

session = None


def send_request(item1, item2):
    payload = {"first": item1, "second": item2}
    url = "https://neal.fun/api/infinite-craft/pair"
    global session
    if session is None:
        session = create_session()
    session.headers.update({"Referer": "https://neal.fun/infinite-craft/"})
    x = session.get(url, params=payload)
    return x


def parse_json(json_body, key):
    value = ""
    try:
        value = json_body[key]
    except KeyError:
        print("Missing '" + key + "' key in JSON data")
    finally:
        return value


def create_session():
    print("Creating Session")
    url = "https://neal.fun/api/infinite-craft"
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
            "Host": "neal.fun",
        }
    )
    r = session.get(url)
    return session
