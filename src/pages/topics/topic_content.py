from pathlib import Path
from dataclasses import dataclass

from helpers import read_json, write_json
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

    @staticmethod
    def get_matching_topic(name: str) -> int:
        """Fetches or, if one does not exist, creates a given topic."""
        topics: dict = read_json("assets/mock_data/topics.json")

        for topic in topics["topics"]:
            if topic["name"] == name:
                return topic["id"]

        id = topics["topics"][-1]["id"] + 1
        topics["topics"].append(
            {
                "id": id,
                "name": name
            }
        )

        write_json("assets/mock_data/topics.json", topics)
        return id