from pathlib import Path
from dataclasses import dataclass

from helpers import read_json
from pages.posts.post_content import PostContent

@dataclass
class TopicContent():
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    @classmethod
    def load_topics(cls, filepath: Path | str) -> list["TopicContent"]:
        data: list[dict] = read_json(filepath)["topics"]
        topics = []
        for topic in data:
            topics.append(cls(
                id=topic["id"],
                name=topic["name"]
            ))
        return topics

    @staticmethod
    def get_posts_by_topic(topic_id: int) -> list[PostContent]:
        posts = PostContent.load_posts("assets/mock_data/posts.json")
        return [post for post in posts if post.topic == topic_id]