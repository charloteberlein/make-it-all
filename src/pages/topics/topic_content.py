from pathlib import Path
from dataclasses import dataclass

from helpers import read_json, write_json
from pages.posts.post_content import PostContent

@dataclass
class TopicContent():
    def __init__(self, id: int, name: str, writable: bool):
        self.id = id
        self.name = name
        self.writable = writable

    @classmethod
    def load_topics(cls, filepath: Path | str = "assets/mock_data/topics.json") -> list["TopicContent"]:
        data: list[dict] = read_json(filepath)["topics"]
        topics = []
        for topic in data:
            topics.append(cls(
                id=topic["id"],
                name=topic["name"],
                writable=topic["writable"]
            ))
        return topics

    @staticmethod
    def save_topics(filepath: Path | str, topics: list[TopicContent]) -> None:
        data = []
        for topic in topics:
            data.append({
                "id": topic.id,
                "name": topic.name,
                "writable": topic.writable
            })
        write_json(filepath, {"topics": data})

    @staticmethod
    def get_writable_topics() -> list[TopicContent]:
        return [
            topic for topic in TopicContent.load_topics()
            if topic.writable
        ]

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
                "name": name,
                "writable": True
            }
        )

        write_json("assets/mock_data/topics.json", topics)
        return id

    @staticmethod
    def get_topic_name(topic_id: int) -> str:
        topics = TopicContent.load_topics()
        result = [topic.name for topic in topics if topic.id == topic_id]
        return result[0] if result else ""

    @staticmethod
    def get_topic_writable(topic_id: int) -> bool:
        topics = TopicContent.load_topics()
        return any(topic.id == topic_id and topic.writable for topic in topics)

    @staticmethod
    def set_topic_writable(topic_id: int, writable: bool) -> None:
        topics = TopicContent.load_topics()
        for topic in topics:
            if topic.id == topic_id:
                topic.writable = writable
        TopicContent.save_topics("assets/mock_data/topics.json", topics)