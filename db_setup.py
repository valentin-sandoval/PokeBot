
import sqlite3, requests

DB = "pokemon.db"
API = "https://pokeapi.co/api/v2/pokemon/"

def create_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
      CREATE TABLE IF NOT EXISTS pokemon (
        id   INTEGER PRIMARY KEY,
        nombre TEXT UNIQUE,
        altura REAL,
        peso   REAL,
        tipos  TEXT,
        habilidades TEXT
      )
    """)
    conn.commit()
    conn.close()

def fetch_and_store(limit=151):
    conn = sqlite3.connect(DB)
    c    = conn.cursor()
    for i in range(1, limit+1):
        r = requests.get(f"{API}{i}")
        if r.status_code != 200: continue
        d = r.json()
        tipos = ",".join([t["type"]["name"] for t in d["types"]])
        habs  = ",".join([h["ability"]["name"] for h in d["abilities"]])
        c.execute("""
          INSERT OR IGNORE INTO pokemon
          (id,nombre,altura,peso,tipos,habilidades)
          VALUES (?,?,?,?,?,?)
        """, (d["id"], d["name"], d["height"], d["weight"], tipos, habs))
        print("Guardado:", d["name"])
    conn.commit()
    conn.close()
    print("✅ Base lista con", limit, "Pokémons.")

if __name__ == "__main__":
    create_db()
    fetch_and_store()
