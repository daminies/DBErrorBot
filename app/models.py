
# models.py
from pydantic import BaseModel

class errorlog(BaseModel):
    title: str
    content: str


