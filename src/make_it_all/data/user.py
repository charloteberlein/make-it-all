import re
from dataclasses import asdict, dataclass
from typing import Any, cast

from loguru import logger

from make_it_all.data.json_store import DATA_DIR, read_json, write_json

USERS_JSON_PATH = DATA_DIR / "users.json"


@dataclass
class User:
    id: int
    name: str
    email: str
    password: str
    rank: str


def _load_users() -> list[User]:
    data = cast(dict[str, list[dict[str, Any]]], read_json(USERS_JSON_PATH))
    return [User(**entry) for entry in data["users"]]


def _save_users(users: list[User]) -> None:
    write_json(USERS_JSON_PATH, {"users": [asdict(user) for user in users]})


def find_user(email: str, password: str) -> User | None:
    """Finds matching user and password in users.JSON"""
    for user in _load_users():
        if user.email.lower() == email.strip().lower() and user.password == password:
            return user


def find_email(email: str) -> bool:
    """Checks if the email exists in users.JSON -> for registration."""
    try:
        return any(user.email.strip().lower() == email.strip().lower() for user in _load_users())
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        logger.exception("Could not find user email.")
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
    return re.search(r'[!@#$%^&*(),.?":{}|<>\-_=+~`[\]\\;\/]', password) is not None


def add_user_password(email: str, password: str) -> bool:
    """Updates the users.JSON file with new password -> for forgot password."""
    try:
        users = _load_users()
        for user in users:
            if user.email.strip().lower() == email.strip().lower():
                user.password = password
                _save_users(users)
                return True
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        logger.exception("Could not update user password.")
    return False


def create_user_account(email: str, firstname: str, lastname: str, password: str) -> bool:
    """Adds user's name and passowrd to users.JSON -> for Account registration page."""
    try:
        users = _load_users()
        for user in users:
            if user.email.strip().lower() == email.strip().lower():
                if user.password:
                    return False

                user.name = f"{firstname.strip()} {lastname.strip()}"
                user.password = password
                _save_users(users)
                return True
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        logger.exception("Could not create user account.")
    return False


def validate_registration_inputs(
    email: str, firstname: str, lastname: str, password: str, confirm_password: str
) -> str | None:
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
    return next((user for user in _load_users() if user.id == user_id), None)
