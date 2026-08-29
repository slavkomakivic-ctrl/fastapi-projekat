from pydantic import BaseModel

class Knjiga(BaseModel):
    naslov: str
    godina: int
    ocjena: int