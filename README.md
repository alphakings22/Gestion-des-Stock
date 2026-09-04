APHA Gestion Stock — Système de Gestion de Stock

Application desktop développée en **Python** pour la gestion complète d'un stock de produits multi-catégories : inventaire, fournisseurs, commandes d'approvisionnement et alertes de rupture.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)

📋Fonctionnalités

- **Tableau de bord** : statistiques en temps réel (nombre de produits, catégories, fournisseurs, commandes, valeur totale du stock, alertes actives)
- **Gestion des produits** : ajout, modification, suppression, recherche et filtrage par catégorie, seuil d'alerte personnalisable par produit
- **Gestion des catégories** : organisation du stock par famille de produits
- **Gestion des fournisseurs** : CRUD complet (nom, téléphone, email)
- **Gestion des commandes d'approvisionnement** : création de commandes liées à un fournisseur, suivi de statut (En attente, Reçue, etc.), calcul automatique du total
- **Système d'alertes** : détection automatique des produits dont la quantité est en dessous du seuil défini

🛠️ Stack technique

| Composant | Technologie |
|---|---|
| Langage | Python 3 |
| Interface graphique | Tkinter (ttk pour les tableaux) |
| Base de données | SQLite3 |
| Architecture | Séparation logique métier (`database.py`) / interface (`app.py`) |

📂 Structure du projet

```
gestion-stock/
├── main.py       # Point d'entrée de l'application
├── app.py        # Interface graphique (Tkinter) + design system
├── database.py   # Couche d'accès aux données (SQLite)
└── stock.db      # Base de données (générée automatiquement)
```

🚀 Installation et lancement

```bash
# Cloner le dépôt
git clone https://github.com/[ton-username]/gestion-stock.git
cd gestion-stock

# Lancer l'application (aucune dépendance externe, Tkinter inclus avec Python)
python main.py
```

La base de données SQLite est créée et remplie automatiquement avec des données de démonstration au premier lancement.

🎨 Design

Interface personnalisée avec un thème "Togo Moderne" : palette orange-rouge et or, sidebar sombre, cartes statistiques, tableaux stylisés — entièrement codée à la main sans framework UI externe.

👤 Auteur

Développé par Kwueku Bentsi Jucal Johnson
