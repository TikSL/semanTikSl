# T outes les fonctions liées aux dictionnaires

from gensim.models import KeyedVectors
import random

def get_dico(dico):
    fichier = open(dico, 'r', encoding='utf-8')
    lignes = fichier.readlines()
    liste = []
    for mot in lignes:
        liste.append(mot[:-1])
    fichier.close()
    return liste

def get_modele(vecteurs):
    modele = KeyedVectors.load_word2vec_format(vecteurs, binary=True, unicode_errors="ignore")
    return modele

def get_mot_mystere(partie):
    try:
        fichier = open(partie.dictionnaire_mot_mystere, 'r', encoding='utf-8')
        mots = fichier.readlines()
        n = len(mots)
        rd = random.randint(0, n - 1)
        mm = mots[rd][:-1]
        fichier.close()
        return mm
    except KeyError:
        get_mot_mystere(partie)

