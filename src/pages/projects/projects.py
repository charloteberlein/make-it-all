from pathlib import Path
from dataclasses import dataclass


from helpers import read_json

@dataclass
class Project():
    def __init__(
            self, project_id : int, name: str, progress: int, total_time: int, time_taken: int
    ): 
        self.project_id = project_id
        self.name = name                
        self.progress = progress
        self.total_time = total_time # in minutes
        self.time_taken = time_taken # in minutes

    @property
    def timePercentage(self):
        if self.total_time <= 0:
            return 0

        return (self.time_taken / self.total_time ) * 100