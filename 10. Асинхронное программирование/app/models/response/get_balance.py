from pydantic import BaseModel


class GetBalance(BaseModel):
    balance: int
