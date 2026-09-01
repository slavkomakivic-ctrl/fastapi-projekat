from fastapi import APIRouter, HTTPException
from database import kursor, konekcija
from models import Knjiga, Korisnik
from auth import hesuj_lozinku

router = APIRouter()

@router.post("/registracija")
def registruj_korisnika(korisnik: Korisnik):
    hash_lozinke = hesuj_lozinku(korisnik.lozinka)
    kursor.execute(
        "INSERT INTO korisnici (korisnicko_ime, lozinka_hash) VALUES (?, ?)",
        (korisnik.korisnicko_ime, hash_lozinke)
    )
    konekcija.commit()
    return {"poruka": f"Registrovan korisnik: {korisnik.korisnicko_ime}"}

@router.get("/korisnici")
def prikazi_sve_korisnike():
    kursor.execute("SELECT * FROM korisnici")
    rezultati = kursor.fetchall()
    return {"korisnici": rezultati}

@router.post("/knjige")
def dodaj_knjigu(knjiga: Knjiga):
    kursor.execute(
        "INSERT INTO knjige (naslov, godina, ocjena) VALUES (?, ?, ?)",
        (knjiga.naslov, knjiga.godina, knjiga.ocjena)
    )
    konekcija.commit()
    return {"poruka": f"Dodata knjiga: {knjiga.naslov}"}

@router.get("/knjige")
def prikazi_sve():
    kursor.execute("SELECT * FROM knjige")
    rezultati = kursor.fetchall()
    return {"knjige": rezultati}

@router.delete("/knjige/{id}")
def obrisi_knjigu(id: int):
    kursor.execute("SELECT * FROM knjige WHERE id = ?", (id,))
    postoji = kursor.fetchone()

    if postoji is None:
        raise HTTPException(status_code=404, detail="knjiga sa tim brojem id ne postoji")

    kursor.execute("DELETE FROM knjige WHERE id = ?", (id,))
    konekcija.commit()
    return {"poruka": f"Obrisana knjiga sa id {id}"}

@router.put("/knjige/{id}")
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

@router.get("/knjige/{id}")
def prikazi_knjigu_id(id: int):
    kursor.execute("SELECT * FROM knjige WHERE id = ?", (id,))
    knjiga = kursor.fetchone()

    if knjiga is None:
        raise HTTPException(status_code=404, detail="knjiga sa tim brojem id ne postoji")

    return {"knjiga": knjiga}