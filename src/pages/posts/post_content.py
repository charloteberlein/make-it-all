from pathlib import Path
from dataclasses import dataclass

from helpers import read_json

@dataclass
class PostContent():
    def __init__(
        self, id: int, viewed: bool, date_created: str, topic: int, title: str, content: str
    ):
        self.id = id
        self.viewed = viewed                # TODO: Add notifications for posts not yet viewed.
        self.date_created = date_created
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