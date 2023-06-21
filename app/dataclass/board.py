from dataclasses import dataclass
from typing import Optional


@dataclass
class Board:
    board: str | int
    num: str
    article_url: str
    writer: Optional[str] = None
    is_importance: Optional[bool] = None
