from pydantic import BaseModel
from typing import List


class PairsContent(BaseModel):
    content: List[str]
