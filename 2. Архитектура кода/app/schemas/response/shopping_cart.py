from pydantic import BaseModel


class ProblemItem(BaseModel):
    item_id: str
    problem: str

