from pydantic import BaseModel


class ACKOrderResponse(BaseModel):
    symbol: str
    orderId: int


class FullOrderResponse(BaseModel):
    symbol: str
    orderId: int
    price: str
    executedQty: str
    status: str
