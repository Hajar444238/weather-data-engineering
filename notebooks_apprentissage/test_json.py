import json
import csv 
from main import PROCESSED_DIR, RAW_DIR

rabat = {"ville": "Rabat", "température": 25, "humidité": 60, "date": "30/09/2026"}
chemin = RAW_DIR / "test_rabat.json"
with open(chemin, "w", encoding="utf-8") as f:
    json.dump(rabat, f, indent=4, ensure_ascii=False) # dump fait ecrir le dictionnaire dans le fichier json

with open(chemin, "r", encoding="utf-8") as f:
    donnees = json.load(f) # load lit le fichier json et le transforme en dictionnaire Python
    print(donnees)
    print(donnees["température"]) 
    print(type(donnees))

casa = {"ville": "Casablanca", "température": 30, "humidité": 50, "date": "30/09/2026"} 
chemin2 = RAW_DIR / "test_casablanca.json"
with open (chemin2, "w", encoding="utf-8") as f:
    json.dump(casa, f, indent=4, ensure_ascii=False)

tanger = {"ville": "Tanger", "température": 28, "humidité": 55, "date": "30/09/2026"}
chemin3 = RAW_DIR / "test_tanger.json"
with open (chemin3, "w", encoding="utf-8") as f:
    json.dump(tanger, f, indent=4, ensure_ascii=False)


for fichier in RAW_DIR.glob("*.json"): # glob() = méthode qui permet de lister les fichiers d'un dossier selon un motif (ici tous les fichiers json)
    print(fichier.name)

toutes_les_villes = []
for fichier in RAW_DIR.glob("*.json"): 
    with open(fichier, "r", encoding="utf-8") as f:
        ville = json.load(f)
        toutes_les_villes.append(ville) 

print(toutes_les_villes)
print(len(toutes_les_villes)) 
print(type(toutes_les_villes[0]))

# ecriture du fichier csv
print("Ecriture du fichier csv :")
chemin_csv = PROCESSED_DIR / "villes.csv"
with open(chemin_csv, "w",newline="", encoding="utf-8") as f: # newline="" = pour éviter les lignes vides entre chaque ligne du csv
    writer = csv.DictWriter(f, fieldnames=["ville", "température", "humidité", "date"]) # 
    writer.writeheader() # writeheader() = écrit la première ligne du fichier csv avec les noms des colonnes
    writer.writerows(toutes_les_villes) # writerows() = écrit plusieurs lignes à la fois (ici toutes les villes)

# lecture du fichier csv
print("Lecture du fichier csv :")
with open(chemin_csv, "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f) # DictReader() = lit le fichier csv et le transforme en dictionnaire Python
    for ligne in reader:
        print(ligne)
        print(type(ligne))  
        print(type(ligne["température"]))
        print(type(ligne["ville"]))
