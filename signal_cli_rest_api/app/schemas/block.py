from typing import Optional, List
from pydantic import BaseModel


class Block(BaseModel):
    numbers: List[str]
    group: Optional[bool] = False
