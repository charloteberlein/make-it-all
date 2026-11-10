import re
from dataclasses import dataclass

from make_it_all.data.json_store import DATA_DIR, read_json, write_json

USERS_JSON_PATH = DATA_DIR / "users.json"


@dataclass
class User:
    id: int
    name: str
    email: str
    password: str
    rank: str


def find_user(email: str, password: str) -> User | None:
    """Finds matching user and password in users.JSON"""
    data = read_json(USERS_JSON_PATH)

    for entry in data["users"]:
        if entry["email"].lower() == email.strip().lower() and entry["password"] == password:
            return User(**entry)


def find_email(email: str) -> bool:
    """Checks if the email exists in users.JSON -> for registration."""
    try:
        data = read_json(USERS_JSON_PATH)
        for user in data.get("users", []):
            if user.get("email", "").strip().lower() == email.strip().lower():
                return True
    except Exception:
        pass
    return False


def is_strong_password(password: str) -> bool:
    """Checks if the set password meets the strength requirements."""
    if len(password) < 10:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if len(re.findall(r"\d", password)) < 2:
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>\-_=+~`[\]\\;\/]', password):
        return False
    return True


def add_user_password(email: str, password: str) -> bool:
    """Updates the users.JSON file with new password -> for forgot password."""
    try:
        data = read_json(USERS_JSON_PATH)
        updated = False

        for user in data.get("users", []):
            if user.get("email", "").strip().lower() == email.strip().lower():
                user["password"] = password
                updated = True
                break
        if updated:
            write_json(USERS_JSON_PATH, data)
            return True
    except Exception:
        pass
    return False


def create_user_account(email: str, firstname: str, lastname: str, password: str) -> bool:
    """Adds user's name and passowrd to users.JSON -> for Account registration page."""
    try:
        data = read_json(USERS_JSON_PATH)

        for user in data.get("users", []):
            if user.get("email", "").strip().lower() == email.strip().lower():
                if user.get("password"):
                    return False

                user["name"] = f"{firstname.strip()} {lastname.strip()}"
                user["password"] = password
                write_json(USERS_JSON_PATH, data)
                return True
    except Exception:
        pass
    return False


def validate_registration_inputs(
    email: str, firstname: str, lastname: str, password: str, confirm_password: str
):
    """Validates fields -> for Account Registration page."""
    if not email or not firstname or not lastname or not password or not confirm_password:
        return "❌ Please fill in all fields."

    if not email.endswith("@make-it-all.co.uk"):
        return "❌ Registration is restricted to @make-it-all.co.uk emails."

    if not find_email(email):
        return "❌ Email not found in our company records."

    if password != confirm_password:
        return "❌ Passwords do not match."

    if not is_strong_password(password):
        return "❌ Password must be 10+ characters long \n(incl. Uppercase, lowercase with at least 2 numbers & a symbol)."
    return None


def validate_reset_password(email: str, password: str, confirm_password: str) -> str | None:
    """Validates fields -> for Forgot Password page."""
    if not email or not password or not confirm_password:
        return "❌ Please fill in all fields."

    if not email.endswith("@make-it-all.co.uk"):
        return "❌ Registration is restricted to @make-it-all.co.uk emails."

    if not find_email(email):
        return "❌ This email address is not registered in the system."

    if password != confirm_password:
        return "❌ Passwords do not match."

    if not is_strong_password(password):
        return "❌ Password must be 10+ characters long \n(incl. Uppercase, lowercase with at least 2 numbers & a symbol)."
    return None


def get_user_by_id(user_id: int | None) -> User | None:
    if user_id is None:
        return None
    for entry in read_json(DATA_DIR / "users.json")["users"]:
        if entry["id"] == user_id:
            return User(**entry)
