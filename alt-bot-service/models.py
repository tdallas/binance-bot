from pydantic import BaseModel
from typing import List
from datetime import datetime
from decimal import *


class PairContent(BaseModel):
    pair: str
    date: str


class PairsContent(BaseModel):
    content: List[PairContent]


class SetBuyPriceBody(BaseModel):
    pair: str
    buy_price: Decimal


class Pair(BaseModel):
    pair: str
    date: datetime
    traded: bool
    buy_price: Decimal
