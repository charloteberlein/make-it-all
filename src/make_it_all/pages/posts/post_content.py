from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from make_it_all.helpers import read_json, write_json


@dataclass
class PostContent:
    def __init__(
        self, id: str, viewed: bool, date_created: str, archived: bool, topic: str, title: str,
        content: str, created_by: int| None = None, upvote_count: int = 0, upvoted_users: list[int] = None
    ):
        # Metadata
        self.id = id
        self.viewed = viewed                # TODO: Add notifications for posts not yet viewed.
        self.date_created = date_created
        self.created_by = created_by
        self.archived = archived
        # Content
        self.title = title
        self.topic = topic
        self.content = content
        self.upvote_count = upvote_count
        self.upvoted_users = upvoted_users or []

    def serialise(self) -> dict:
        """Serialises a `PostContent` object to a dictionary for it to be saved to a JSON."""
        return {
            "metadata": {
                "id": self.id,
                "viewed": self.viewed,
                "date-created": self.date_created,
                "created_by": self.created_by,
                "archived": self.archived
            },
            "title": self.title,
            "topic": self.topic,
            "content": self.content,
            "upvote_count": self.upvote_count,
            "upvoted_users": self.upvoted_users
        }

    @classmethod
    def load_posts(cls, filepath: Path | str) -> list["PostContent"]:
        """Deserialises the JSON object into a list of `PostContent` objects."""
        data: list[dict] = read_json(filepath)["posts"]
        posts = []
        for post in data:
            posts.append(cls(
            id=post["metadata"]["id"],
                viewed=post["metadata"]["viewed"],
                date_created=post["metadata"]["date-created"],
                created_by=post["metadata"].get("created_by"),
                archived=post["metadata"]["archived"],
                topic=post["topic"],
                title=post["title"],
                content=post["content"],
                upvote_count=post.get("upvote_count", 0),
                upvoted_users=post.get("upvoted_users", [])
            ))
        return posts

    @classmethod
    def get_post_by_id(cls, id: str) -> "PostContent | None":
        posts = cls.load_posts("assets/mock_data/posts.json")
        for post in posts:
            if post.id == id:
                return post
        return None

    @classmethod
    def get_recent_posts(cls, count: int = 5) -> list["PostContent"]:
        posts = cls.load_posts("assets/mock_data/posts.json")
        newest_first = sorted(
            posts,
            key=lambda post: (datetime.strptime(post.date_created, "%d-%m-%Y"), post.id),
            reverse=True,
        )
        return newest_first[:count]

    @classmethod
    def get_posts_by_user(cls, user_id: int | None) -> list["PostContent"]:
        if user_id is None:
            return []

        posts = cls.load_posts("assets/mock_data/posts.json")
        mine = [post for post in posts if post.created_by == user_id]
        return sorted(
            reversed(mine),
            key=lambda post: datetime.strptime(post.date_created, "%d-%m-%Y"),
            reverse=True,
        )

    @classmethod
    def archive_post(cls, post_id: str, archive: bool) -> None:
        posts = cls.load_posts("assets/mock_data/posts.json")
        post = next(post for post in posts if post.id == post_id)
        post.archived = archive
        write_json("assets/mock_data/posts.json", {"posts": [post.serialise() for post in posts]})

    @classmethod
    def delete_post(cls, post_id: str) -> str:
        posts = cls.load_posts("assets/mock_data/posts.json")
        deleted_post = next(post for post in posts if post.id == post_id)
        write_json(
            "assets/mock_data/posts.json",
            {"posts": [post.serialise() for post in [post for post in posts if post.id != post_id]]}
        )
        return deleted_post.topic

    @classmethod
    def upvote_post(cls, post_id: str, user_id: int) -> tuple[int, bool]:
        posts = cls.load_posts("assets/mock_data/posts.json")
        for post in posts:
            if post.id == post_id:
                # Toggle logic for upvote button.
                if user_id in post.upvoted_users:
                    post.upvoted_users.remove(user_id)
                    post.upvote_count = max(0, post.upvote_count - 1)
                    write_json(
                        "assets/mock_data/posts.json",
                        {"posts": [p.serialise() for p in posts]}
                    )
                    return post.upvote_count, False

                post.upvoted_users.append(user_id)
                post.upvote_count += 1

                write_json(
                    "assets/mock_data/posts.json",
                    {"posts": [p.serialise() for p in posts]}
                )
                return post.upvote_count, True
        return 0, False
        
