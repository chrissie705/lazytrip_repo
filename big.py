import sys
import pymongo
from pymongo import MongoClient

connection = MongoClient("ds149344.mlab.com", 49344)
db = connection["lazytrip_dev"]
db.authenticate("test", "firstival1")

activities = db.activities
profils = db.profils

nb_gens = 11
nb_films = 2600
notes = [[0] * nb_films for _ in range(nb_gens)]
prenoms = list(range(nb_gens))
films = [''] * nb_films
NB_VOISINS = 5
NB_PREDICTIONS = 30

nb_gens = 0
nb_films = 0
nb_notes = 0

for profil in profils.find({}, {"idProfil":1, "note":1, "idActivity":1}):
    i = int(profil["idProfil"])
    i_film = int(profil["idActivity"])
    note = int(profil["note"])
    notes[i][i_film] = note
    nb_gens = max(i + 1, nb_gens)
    nb_films = max(i_film + 1, nb_films)
    nb_notes += 1
    
print(nb_notes, 'notes chargées de', nb_gens, 'personnes sur', nb_films, 'films')

for activity in activities.find({}, {"name": 1, "idActivity": 1}):
    id_activity = activity['idActivity']
    titre = activity['name']
    films[int(id_activity)] = titre

    