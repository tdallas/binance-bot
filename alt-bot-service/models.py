from pydantic import BaseModel
from typing import List
from datetime import datetime

class PairContent(BaseModel):
    pair: str
    date: str

class PairsContent(BaseModel):
    content: List[PairContent]
