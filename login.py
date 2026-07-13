import json
import os

FILE = "users.json"


def load_users():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []


def save_users(users):
    with open(FILE, "w") as f:
        json.dump(users, f, indent=4)


def signup(username, password):

    users = load_users()

    for user in users:
        if user["username"] == username:
            return False

    users.append(
        {
            "username": username,
            "password": password
        }
    )

    save_users(users)

    return True


def login(username, password):

    users = load_users()

    for user in users:

        if (
            user["username"] == username
            and
            user["password"] == password
        ):
            return True

    return False