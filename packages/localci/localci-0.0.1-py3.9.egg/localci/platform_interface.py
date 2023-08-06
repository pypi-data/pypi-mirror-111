from dataclasses import dataclass
from typing import Tuple


@dataclass
class Platform:

    def __init__(self):
        pass

    project_name: str
    project_version: str

    def make(self) -> None:
        pass

    def get_project_info(self) -> Tuple[str, str]:
        pass