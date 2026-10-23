from dataclasses import dataclass

from helpers import read_json

@dataclass
class User:
    id: int
    name: str
    email: str
    password: str
    rank: str


def find_user(email: str, password: str) -> User  |  None:
    data = read_json("assets/mock_data/users.json")

    for entry in data["users"]:
        if entry["email"].lower() == email.strip().lower() and entry["password"] == password:
            return User(**entry)

    return None

def get_user_by_id(user_id: int | None) -> User  |  None:
    if user_id is None:
        return None
    for entry in read_json("assets/mock_data/users.json")["users"]:
        if entry["id"] == user_id:
            return User(**entry)

    return None