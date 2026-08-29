from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Knjiga(BaseModel):
    naslov: str
    godina: int
    ocjena: int

konekcija = sqlite3.connect("biblioteka_api.db", check_same_thread=False)
kursor = konekcija.cursor()
kursor.execute("""
    CREATE TABLE IF NOT EXISTS knjige (
        id INTEGER PRIMARY KEY,
        naslov TEXT,
        godina INTEGER,
        ocjena INTEGER
    )
""")
konekcija.commit()

@app.post("/knjige")
def dodaj_knjigu(knjiga: Knjiga):
    kursor.execute(
        "INSERT INTO knjige (naslov, godina, ocjena) VALUES (?, ?, ?)",
        (knjiga.naslov, knjiga.godina, knjiga.ocjena)
    )
    konekcija.commit()
    return {"poruka": f"Dodata knjiga: {knjiga.naslov}"}

@app.get("/knjige")
def prikazi_sve():
    kursor.execute("SELECT * FROM knjige")
    rezultati = kursor.fetchall()
    return {"knjige": rezultati}

@app.delete("/knjige/{id}")
def obrisi_knjigu(id: int):
    kursor.execute("SELECT * FROM knjige WHERE id = ?", (id,))
    postoji = kursor.fetchone()

    if postoji is None:
        raise HTTPException(status_code=404, detail="knjiga sa tim brojem id ne postoji")

    kursor.execute("DELETE FROM knjige WHERE id = ?", (id,))
    konekcija.commit()
    return {"poruka": f"Obrisana knjiga sa id {id}"}

@app.put("/knjige/{id}")
def azuriraj_knjigu(id: int, knjiga: Knjiga):
    kursor.execute("SELECT * FROM knjige WHERE id = ?", (id,))
    postoji = kursor.fetchone()

    if postoji is None:
        raise HTTPException(status_code=404, detail="knjiga sa tim brojem id ne postoji")

    kursor.execute(
        "UPDATE knjige SET naslov = ?, godina = ?, ocjena = ? WHERE id = ?",
        (knjiga.naslov, knjiga.godina, knjiga.ocjena, id)
    )
    konekcija.commit()
    return {"poruka": f"Azurirana knjiga sa id {id}"}

@app.get("/knjige/{id}")
def prikazi_knjigu_id(id: int):
    kursor.execute("SELECT * FROM knjige WHERE id = ?", (id,))
    knjiga = kursor.fetchone()

    if knjiga is None:
        raise HTTPException(status_code=404, detail="knjiga sa tim brojem id ne postoji")

    return {"knjiga": knjiga}