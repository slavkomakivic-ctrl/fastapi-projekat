from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hesuj_lozinku(lozinka):
    return pwd_context.hash(lozinka)

def provjeri_lozinku(lozinka, hash_iz_baze):
    return pwd_context.verify(lozinka, hash_iz_baze)