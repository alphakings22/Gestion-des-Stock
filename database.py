import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "stock.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS fournisseurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            telephone TEXT,
            email TEXT
        );

        CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prix REAL NOT NULL DEFAULT 0,
            quantite INTEGER NOT NULL DEFAULT 0,
            seuil_alerte INTEGER NOT NULL DEFAULT 5,
            categorie_id INTEGER,
            FOREIGN KEY (categorie_id) REFERENCES categories(id)
        );

        CREATE TABLE IF NOT EXISTS commandes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fournisseur_id INTEGER,
            date TEXT NOT NULL,
            statut TEXT NOT NULL DEFAULT 'En attente',
            FOREIGN KEY (fournisseur_id) REFERENCES fournisseurs(id)
        );

        CREATE TABLE IF NOT EXISTS lignes_commande (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            commande_id INTEGER NOT NULL,
            produit_id INTEGER NOT NULL,
            quantite INTEGER NOT NULL DEFAULT 1,
            prix_unitaire REAL NOT NULL DEFAULT 0,
            FOREIGN KEY (commande_id) REFERENCES commandes(id),
            FOREIGN KEY (produit_id) REFERENCES produits(id)
        );
    """)

    # Données de démonstration
    c.execute("SELECT COUNT(*) FROM categories")
    if c.fetchone()[0] == 0:
        categories = [("Électronique",), ("Alimentation",), ("Vêtements",), ("Mobilier",)]
        c.executemany("INSERT INTO categories (nom) VALUES (?)", categories)

        fournisseurs = [
            ("TechSupply SA", "01 23 45 67 89", "contact@techsupply.fr"),
            ("FoodPro SARL", "01 98 76 54 32", "info@foodpro.fr"),
            ("ModeTex", "01 11 22 33 44", "ventes@modetex.fr"),
        ]
        c.executemany("INSERT INTO fournisseurs (nom, telephone, email) VALUES (?,?,?)", fournisseurs)

        produits = [
            ("Laptop Dell 15\"", 799.99, 12, 3, 1),
            ("Souris sans fil", 29.99, 45, 10, 1),
            ("Clavier mécanique", 89.99, 2, 5, 1),
            ("Café Arabica 1kg", 12.50, 80, 20, 2),
            ("Chocolat noir 72%", 3.99, 4, 15, 2),
            ("T-shirt coton M", 19.99, 30, 10, 3),
            ("Chaise de bureau", 249.99, 8, 2, 4),
        ]
        c.executemany("INSERT INTO produits (nom, prix, quantite, seuil_alerte, categorie_id) VALUES (?,?,?,?,?)", produits)

    conn.commit()
    conn.close()

# ─── PRODUITS ───────────────────────────────────────────────
def get_produits(search="", categorie_id=None):
    conn = get_connection()
    q = """SELECT p.*, c.nom as categorie FROM produits p
           LEFT JOIN categories c ON p.categorie_id = c.id
           WHERE p.nom LIKE ?"""
    params = [f"%{search}%"]
    if categorie_id:
        q += " AND p.categorie_id = ?"
        params.append(categorie_id)
    q += " ORDER BY p.nom"
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return rows

def add_produit(nom, prix, quantite, seuil, categorie_id):
    conn = get_connection()
    conn.execute("INSERT INTO produits (nom, prix, quantite, seuil_alerte, categorie_id) VALUES (?,?,?,?,?)",
                 (nom, prix, quantite, seuil, categorie_id))
    conn.commit(); conn.close()

def update_produit(id, nom, prix, quantite, seuil, categorie_id):
    conn = get_connection()
    conn.execute("UPDATE produits SET nom=?, prix=?, quantite=?, seuil_alerte=?, categorie_id=? WHERE id=?",
                 (nom, prix, quantite, seuil, categorie_id, id))
    conn.commit(); conn.close()

def delete_produit(id):
    conn = get_connection()
    conn.execute("DELETE FROM produits WHERE id=?", (id,))
    conn.commit(); conn.close()

# ─── CATEGORIES ─────────────────────────────────────────────
def get_categories():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM categories ORDER BY nom").fetchall()
    conn.close()
    return rows

def add_categorie(nom):
    conn = get_connection()
    conn.execute("INSERT INTO categories (nom) VALUES (?)", (nom,))
    conn.commit(); conn.close()

def delete_categorie(id):
    conn = get_connection()
    conn.execute("DELETE FROM categories WHERE id=?", (id,))
    conn.commit(); conn.close()

# ─── FOURNISSEURS ────────────────────────────────────────────
def get_fournisseurs():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM fournisseurs ORDER BY nom").fetchall()
    conn.close()
    return rows

def add_fournisseur(nom, tel, email):
    conn = get_connection()
    conn.execute("INSERT INTO fournisseurs (nom, telephone, email) VALUES (?,?,?)", (nom, tel, email))
    conn.commit(); conn.close()

def update_fournisseur(id, nom, tel, email):
    conn = get_connection()
    conn.execute("UPDATE fournisseurs SET nom=?, telephone=?, email=? WHERE id=?", (nom, tel, email, id))
    conn.commit(); conn.close()

def delete_fournisseur(id):
    conn = get_connection()
    conn.execute("DELETE FROM fournisseurs WHERE id=?", (id,))
    conn.commit(); conn.close()

# ─── COMMANDES ───────────────────────────────────────────────
def get_commandes():
    conn = get_connection()
    rows = conn.execute("""
        SELECT c.*, f.nom as fournisseur,
               COUNT(lc.id) as nb_lignes,
               SUM(lc.quantite * lc.prix_unitaire) as total
        FROM commandes c
        LEFT JOIN fournisseurs f ON c.fournisseur_id = f.id
        LEFT JOIN lignes_commande lc ON c.id = lc.commande_id
        GROUP BY c.id ORDER BY c.date DESC
    """).fetchall()
    conn.close()
    return rows

def add_commande(fournisseur_id, date, statut):
    conn = get_connection()
    c = conn.execute("INSERT INTO commandes (fournisseur_id, date, statut) VALUES (?,?,?)",
                     (fournisseur_id, date, statut))
    conn.commit()
    last_id = c.lastrowid
    conn.close()
    return last_id

def update_statut_commande(id, statut):
    conn = get_connection()
    conn.execute("UPDATE commandes SET statut=? WHERE id=?", (statut, id))
    conn.commit(); conn.close()

def delete_commande(id):
    conn = get_connection()
    conn.execute("DELETE FROM lignes_commande WHERE commande_id=?", (id,))
    conn.execute("DELETE FROM commandes WHERE id=?", (id,))
    conn.commit(); conn.close()

def get_lignes_commande(commande_id):
    conn = get_connection()
    rows = conn.execute("""
        SELECT lc.*, p.nom as produit FROM lignes_commande lc
        JOIN produits p ON lc.produit_id = p.id
        WHERE lc.commande_id = ?
    """, (commande_id,)).fetchall()
    conn.close()
    return rows

def add_ligne_commande(commande_id, produit_id, quantite, prix_unitaire):
    conn = get_connection()
    conn.execute("INSERT INTO lignes_commande (commande_id, produit_id, quantite, prix_unitaire) VALUES (?,?,?,?)",
                 (commande_id, produit_id, quantite, prix_unitaire))
    conn.commit(); conn.close()

# ─── STATS ───────────────────────────────────────────────────
def get_stats():
    conn = get_connection()
    stats = {}
    stats['nb_produits'] = conn.execute("SELECT COUNT(*) FROM produits").fetchone()[0]
    stats['nb_categories'] = conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
    stats['nb_fournisseurs'] = conn.execute("SELECT COUNT(*) FROM fournisseurs").fetchone()[0]
    stats['nb_commandes'] = conn.execute("SELECT COUNT(*) FROM commandes").fetchone()[0]
    stats['alertes'] = conn.execute(
        "SELECT COUNT(*) FROM produits WHERE quantite <= seuil_alerte").fetchone()[0]
    stats['valeur_stock'] = conn.execute(
        "SELECT COALESCE(SUM(prix * quantite), 0) FROM produits").fetchone()[0]
    conn.close()
    return stats

def get_alertes():
    conn = get_connection()
    rows = conn.execute("""
        SELECT p.*, c.nom as categorie FROM produits p
        LEFT JOIN categories c ON p.categorie_id = c.id
        WHERE p.quantite <= p.seuil_alerte ORDER BY p.quantite ASC
    """).fetchall()
    conn.close()
    return rows