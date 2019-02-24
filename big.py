import sys
import pymongo
from pymongo import MongoClient

connection = MongoClient("ds149344.mlab.com", 49344)
db = connection["lazytrip_dev"]
db.authenticate("test", "firstival1")

activities = db.activities
profils = db.profils

nb_gens = 24
nb_activites = 2600
notes = [[0] * nb_activites for _ in range(nb_gens)]
prenoms = [''] * nb_gens
activites = [''] * nb_activites
categories = [''] * nb_activites
NB_VOISINS = 5
NB_PREDICTIONS = 15

nb_gens = 0
nb_activites = 0
nb_notes = 0

#Requete pour récupérer la liste des profiles et activités qu'ils ont noté
for profil in profils.find({}, {"idProfil":1, "note":1, "idActivity":1, "prenom":1}):
    i = int(profil["idProfil"])
    i_activite = int(profil["idActivity"])
    note = int(profil["note"])
    notes[i][i_activite] = note #tableau des notes par profil et par activité
    prenoms[i] = profil['prenom']
    nb_gens = max(i + 1, nb_gens)
    nb_activites = max(i_activite + 1, nb_activites)
    nb_notes += 1

print(nb_notes, 'notes chargées de', nb_gens, 'profils sur', nb_activites, 'activités')

#Requete pour récupérer la liste des activites
for activity in activities.find({}, {"name": 1, "idActivity": 1, "categories":1}):
    id_activity = activity['idActivity']
    titre = activity['name']
    activites[int(id_activity)] = titre
    categories[int(id_activity)] = activity['categories'][0]
