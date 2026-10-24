from pathlib import Path
from dataclasses import dataclass

from datetime import datetime

from helpers import read_json

@dataclass
class PostContent():
    def __init__(
        self, id: int, viewed: bool, date_created: str, archived: bool, topic: int, title: str,
        content: str, created_by: int | None = None
    ):
        # Metadata
        self.id = id
        self.viewed = viewed                # TODO: Add notifications for posts not yet viewed.
        self.date_created = date_created
        self.created_by = created_by
        self.archived = archived
        # Content
        self.topic = topic
        self.title = title
        self.content = content

    @classmethod
    def load_posts(cls, filepath: Path | str) -> list["PostContent"]:
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
                content=post["content"]
            ))
        return posts

    @classmethod
    def get_post_by_id(cls, id: int) -> "PostContent | None":
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