# Weather Data Engineering

Pipeline Data Engineering de bout en bout pour l'analyse de données météorologiques :
API Open-Meteo → fichiers bruts (JSON) → Pandas → Parquet / CSV → PostgreSQL.

## Architecture

```
API Open-Meteo → data/raw (JSON) → Pandas (nettoyage, transformation)
              → data/processed (Parquet, CSV) → PostgreSQL (modèle en étoile)
```

![Modèle en étoile](docs/modele en etiole.png)

## Structure du projet

```
weather-data-engineering/
├── data/
│   ├── raw/                 # données brutes, jamais modifiées
│   └── processed/           # données nettoyées (Parquet, CSV)
├── docs/                    # images et documentation
├── notebooks_apprentissage/ # scripts d'essai de l'apprentissage (Phases 1 à 7)
├── src/
│   ├── config.py            # chemins, URL de l'API, villes
│   ├── extract.py           # E : appel API, sauvegarde dans raw/
│   ├── transform.py         # T : nettoyage, colonnes dérivées, merge
│   └── load.py              # L : Parquet, CSV, PostgreSQL
├── .env                     # identifiants de la base (non versionné)
├── main.py                  # point d'entrée : orchestre E, T, L
└── README.md
```

## Installation et lancement

```
pip install requests pandas pyarrow sqlalchemy psycopg2-binary python-dotenv
```

1. Installer PostgreSQL et créer la base `weather_db`.
2. Créer un fichier `.env` à la racine :
```
   DB_USER=postgres
   DB_PASSWORD=votre_mot_de_passe
   DB_HOST=localhost
   DB_PORT=5433
   DB_NAME=weather_db
```
3. Lancer le pipeline depuis la racine : `python main.py`

## Phase 1 : structure et chemins (pathlib)

- `BASE_DIR = Path(__file__).resolve().parent.parent` (dans `src/config.py`) : racine du projet, calculée à partir de l'emplacement du fichier. Le code fonctionne sur n'importe quel ordinateur.
- Un chemin relatif dépend du dossier d'où l'on lance la commande ; `BASE_DIR` non.
- `mkdir(parents=True, exist_ok=True)` : `parents=True` crée aussi le dossier parent manquant, `exist_ok=True` évite l'erreur si le dossier existe déjà (script idempotent).
- Principe **raw / processed** : on ne modifie jamais `raw/`, ce qui permet de tout recalculer en cas de bug (reproductibilité).

## Phase 2 : fichiers

- JSON : `json.dump` (écrire), `json.load` (lire, renvoie un `dict`). `indent=4` et `ensure_ascii=False` pour un fichier lisible avec accents.
- `glob("*.json")` : lister plusieurs fichiers.
- CSV : `csv.DictWriter` / `DictReader`, `newline=""` pour éviter les lignes vides.
- Le CSV ne stocke que du texte : les types sont perdus.

## Phases 3 et 4 : API et ingestion

- API Open-Meteo : gratuite, sans clé ; la ville se choisit par latitude et longitude.
- `requests.get(url, params=..., timeout=10)`, `response.status_code` (200 succès, 404 adresse inconnue, 500+ erreur serveur), `response.json()`.
- Gestion des erreurs : `try / except` pour les pannes réseau, `if status_code == 200` pour les erreurs HTTP.
- Un fichier JSON par ville dans `data/raw/` ; on ne sauvegarde que si la réponse est valide.
- Structure de la réponse : métadonnées à la racine, trois listes de même longueur dans `"hourly"`.

## Phase 5 : Pandas

- `pd.DataFrame(data["hourly"])` : listes JSON vers tableau (72 lignes par ville).
- `pd.to_datetime` (format ISO 8601), `.dt.date`, `.dt.hour`.
- `pd.concat` : un seul tableau de 216 lignes ; colonne `ville` pour distinguer les lignes.
- Nettoyage : `isna()`, `duplicated()`, `rename`.
- Analyse : `groupby`, filtrage, colonne `chaud` (`temperature > 25`), colonne `periode` (`apply`).
- `merge(..., how="left")` pour ajouter la région ; toujours vérifier `len(df)` après un merge.

## Phase 6 : Parquet

- `df.to_parquet(..., index=False)` (nécessite `pyarrow`), `pd.read_parquet`.
- Format binaire, par colonnes, compressé : 9 Ko contre 22 Ko pour le CSV.
- Parquet conserve les types (dates, nombres), pas le CSV.

## Phase 7 : PostgreSQL et modèle en étoile

- PostgreSQL 18 (port 5433), pgAdmin 4, connexion Python via SQLAlchemy + psycopg2.
- Identifiants dans `.env` (jamais dans le code ni sur GitHub), lus avec `python-dotenv`.
- SQL appris : `SELECT`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`, `JOIN`, `CREATE TABLE`, `INSERT`.
  - `WHERE` filtre les lignes avant le regroupement, `HAVING` filtre les groupes après.
  - `COUNT(*)` compte les lignes, `COUNT(col)` ignore les NULL.
- Modèle en étoile : table de faits `meteo` ; dimensions `villes` (ville, region) et `dim_date` (date_, jour, mois), reliées par clés étrangères.

## Phase 8 : ETL modulaire

Le code des phases précédentes est réorganisé en modules, chacun avec une seule responsabilité :

| Module | Rôle |
|---|---|
| `config.py` | constantes : chemins, `API_URL`, `VILLES` (aucune fonction) |
| `extract.py` | `extraire_ville()` renvoie le JSON ou `None` ; `extraire_toutes_les_villes()` sauvegarde dans `raw/` |
| `transform.py` | `transformer()` lit `raw/`, nettoie, enrichit, **renvoie** un DataFrame (ne sauvegarde rien) |
| `load.py` | `charger_parquet`, `charger_csv`, `charger_postgres` |
| `main.py` | appelle E, T, L dans l'ordre ; garde-fou si le tableau est vide |

Points clés :
- On lance toujours le pipeline depuis la racine avec `main.py` : les imports `from src.config import ...` en dépendent.
- `if __name__ == "__main__":` exécute `main()` seulement si le fichier est lancé directement.
- Une ville en échec (`None`) n'arrête pas les autres.

## Limites et améliorations prévues

- `if_exists="replace"` efface la table à chaque exécution : passer à un chargement incrémental sans doublons.
- La colonne `region` est dupliquée dans `meteo` (déjà présente dans `villes`).
- Seulement 3 villes (Rabat, Casablanca, Tanger) : ajouter une ville = une ligne dans `VILLES` et `REGIONS`.
- À venir : Data Quality (Phase 9), logging (10), Git/GitHub (11), tests (12), Docker (13), orchestration (14), dashboard Power BI / Tableau (15).

## Problèmes rencontrés

- Ancien PostgreSQL présent : port 5433 au lieu de 5432.
- Mot de passe oublié : réinitialisé via `pg_hba.conf` (trust, puis retour à scram-sha-256).
- pgAdmin ne démarrait pas : dossiers de configuration AppData renommés.
- `ModuleNotFoundError: src` en lançant `extract.py` directement : lancer `main.py` depuis la racine.

## Phase 9 : Data Quality

Objectif : vérifier automatiquement les données **avant** le chargement. Un pipeline qui charge des données fausses sans alerter est pire qu'un pipeline qui plante.

Fichier : `src/quality.py`, fonction `verifier_qualite(df)` qui **renvoie une liste d'erreurs** (vide si tout est bon). `main()` arrête le pipeline avant le chargement si la liste n'est pas vide.

| Contrôle | Méthode | Ce qu'il détecte |
|---|---|---|
| Valeurs manquantes | `df.isna().sum().sum()` | trous dans les données |
| Doublons | `df.duplicated().sum()` | lignes répétées |
| Températures / humidités | `(~df["col"].between(min, max)).sum()` | valeurs absurdes (ex. 999 °C) |
| Nombre de lignes | `len(VILLES) * FORECAST_DAYS * 24` | ville ou heures manquantes |
| Type de date | `is_datetime64_any_dtype` | colonne `time` mal convertie |

Points clés :
- `between(...)` renvoie `True` pour les valeurs valides ; `~` inverse, donc on compte les invalides.
- Le contrôle du nombre de lignes est le seul à détecter une ville absente (les autres ne voient rien).
- `FORECAST_DAYS` est défini une seule fois dans `config.py` : l'extraction et le contrôle restent cohérents.
- Test réalisé : forcer `temperature = 999` arrête bien le pipeline, sans rien charger.