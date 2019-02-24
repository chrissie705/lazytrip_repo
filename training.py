import warnings
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from big import notes, nb_gens, nb_activites, prenoms, activites, categories, NB_VOISINS, NB_PREDICTIONS

warnings.filterwarnings("ignore", category=FutureWarning)

notes_training, notes_test, prenoms_training, prenoms_test = train_test_split(notes, prenoms, train_size=0.9)
print('###########################################')
print('echantillonage training', len(notes_training))
print('echantillonage test', len(notes_test))
print('###########################################')

#Calcul du score par personne
def score(i, j):
    score = 0
    for k in range(nb_activites):
        score += notes_training[i][k] * notes_training[j][k]
    return score

#Calcul des scores de toutes les personnes
def tous_scores():
    sim = [[0] * len(notes_training) for _ in range(len(notes_training))]
    for i in range(len(notes_training)):
        for j in range(len(notes_training)):
            sim[i][j] = score(i, j)
    return sim

#Calcul des plus proche voisin
def proches_voisins(i):
    candidats = []
    for j in range(len(notes_training)):
        if j != i:
            candidats.append((score(i, j), prenoms_training[j], j))
    candidats.sort()
    print("")
    print('Les', NB_VOISINS, 'profils les plus proches de', prenoms_training[i], 'sont :')
    voisins = []
    for poids, nom, j in candidats[-NB_VOISINS:]:
        print(nom, 'avec poids', poids)
        voisins.append(j)
    return voisins

#Prédiction d'un profil en fonction des voisins
def prediction(i, i_actitive, voisins):
    nb_voisins = 0
    note = 0
    for j in voisins:
        note += notes_training[j][i_actitive]
        nb_voisins += 1
    note /= nb_voisins
    return note

#Calcul de tous les prédictions 
def toutes_predictions(i, voisins):
    candidats = []
    for i_activite in range(nb_activites):
        if notes_training[i][i_activite] == 0:  # Si l'activite n'a pas été vu
            note = prediction(i, i_activite, voisins)
            candidats.append((note, activites[i_activite], categories[i_activite]))
    candidats.sort()
    return candidats[-NB_PREDICTIONS:]

#Recommendation personnalisée
def nouvel_inscrit():
    likes = [0] * nb_activites
    dislikes = [0] * nb_activites
    candidats = []

    for i_activite in range(nb_activites):
        for i in range(len(notes_training)):
            if notes_training[i][i_activite] == 1:
                likes[i_activite] += 1
            elif notes_training[i][i_activite] == -1:
                dislikes[i_activite] += 1
        candidats.append((likes[i_activite] + dislikes[i_activite], activites[i_activite], i_activite))
    candidats.sort() #nombre de votes pour chaque activite

    mon_id = len(notes_training)
    prenom = input('Prénom ? ')
    prenoms_training.append(prenom)

    notes_training.append([0] * nb_activites)  # Nouvelle ligne au tableau de notes
    for _, titre, i_activite in candidats[-10:]:
        note = int(input('As tu aimé %s ? (%d notes) ' % (titre, _)))
        notes_training[mon_id][i_activite] = note
    
    return mon_id

mon_id = nouvel_inscrit()
voisins = proches_voisins(mon_id)
print("#########################")
print("Nous vous recommandons:")
print("")
for ligne in toutes_predictions(mon_id, voisins):
    print(ligne[1], 'dans la catégorie', ligne[2].upper(), 'avec une affinité de', ligne[0]) 
    print("")

x = [""] * len(toutes_predictions(mon_id, voisins))
y = [0] * len(toutes_predictions(mon_id, voisins))

for i, ligne in enumerate(toutes_predictions(mon_id, voisins)):
    x[i] = "A"+str(i+1)
    y[i] = ligne[0]
    print(ligne[1], 'dans la catégorie', ligne[2].upper(), 'avec une affinité de', ligne[0]) 
    print("")

plt.scatter(x, y, s=40, c='red', label='Label 1')
plt.title('Les recommandations')
plt.xlabel('Activités')
plt.ylabel('Affinités')
plt.savefig("reco_graph.png", bbox_inches='tight')
plt.show()
