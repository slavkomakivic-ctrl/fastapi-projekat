from pydantic import BaseModel

class Knjiga(BaseModel):
    naslov: str
    godina: int
    ocjena: int

class Korisnik(BaseModel):
    korisnicko_ime: str
    lozinka: str