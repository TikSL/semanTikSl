# Toutes les fonctions liées à l'affichage, la présentation, le texte etc...

import discord

import sauvegarde

commandes = ('$play', '$ff', '$stop', '$help', '$info', '$regles', '$classement')

content = '**But du jeu :**\n' \
          'Trouver le mot mystère en donnant des mots à la suite.\n' \
          'Un score est attribué à chaque mot envoyé, les milles mots les plus proches sont mis en évidence.\n\n' \
          '\u26A0\uFE0F **Remarques :**\n' \
          'Dans un soucis de clarté, les mots accordés ont été retirés de la liste.\n' \
          'Vous ne cherchez donc qu\'un mot au masculin, au singulier ou non conjugué.\n\n' \
          '\U0001f6a7 **Bugs possibles :**\n' \
          '- Si le bot n\'arrive pas à calculer les 1000 mots les plus proches, ' \
          'il ne commencera pas la partie mais créera un salon. ' \
          'Dans ce cas revenez dans un salon textuel général (là ou vous avez tapé *!play*) et tapez *!stop*. ' \
          'Vous pouvez alors relancer une partie.\n' \
          '- En théorie les accents comptent mais le dictionnaire utilisé est moyen.\n\n' \
          '\U0001f631 : mot le plus proche\n'\
          '\U0001f525 : top 10\n' \
          '\U0001f975 : top 100\n' \
          '\U0001f60e : top 1000\n' \
          '\U0001f976 : pas fou\n\n' \
          '\u2699\uFE0F **Commandes :**\n'\
          '$play : lance une partie\n'\
          '$ff : abandonne pour voir le mot mystère\n' \
          '$stop : arrête la partie sans donner le mot mystère\n' \
          '$regles : affiche ce message\n'\
          '$classement : affiche les joueurs ayant finis une partie\n\n' \
          '	\U0001f340 Bonne chance ! \U0001f340'

embed_regles = discord.Embed(description=content, colour=0x2ecc71)


def infos(partie, commande, utilisateur):
    print(utilisateur, commande)
    print("Joueur avec une partie en cours :")
    for joueur in partie.en_jeu:
        print(joueur.name)
    print("Parties : ")
    for joueur in partie.parties:
        print(joueur.name, joueur.salon, joueur.mot_mystere, joueur.nbr_essais,
              joueur.top1000[0],
              joueur.top1000[1],
              joueur.top1000[2],
              joueur.top1000[3],
              joueur.top1000[4],
              joueur.top1000[5],
              joueur.top1000[6],
              joueur.top1000[7],
              joueur.top1000[8],
              joueur.top1000[9],
              joueur.top1000[998])
    print("------------------")
    return


def emoji(position):
    if position == -1:
        return '\U0001f976'
    elif position > 998:
        return '\U0001f631'
    elif position > 989:
        return '\U0001f525'
    elif position > 899:
        return '\U0001f975'
    else:
        return '\U0001f60e'


def liste_discord(liste):

    num = " "
    mot = " "
    sco = " "
    liste_embed = []
    i = 1
    embed = discord.Embed()

    for x in liste:
        num = num + str(x[0]) + '\n'
        sco = sco + str(x[2]) + '\n'

        if x[3] == -1:
            mot = mot + '.' + '         ' + str(x[4]) + '   ' + str(x[1]) + '\n'
        else:
            mot = mot + '.' + str(x[4]) + '   ' + str(x[3]) + '/1000' + '   ' + str(x[1]) + '\n'

        i += 1
        if i % 21 == 0 or x == liste[-1]:
            embed.add_field(name='n°', value=num, inline=True)
            embed.add_field(name='score', value=sco, inline=True)
            embed.add_field(name='.         mot', value=mot, inline=True)
            liste_embed.append(embed)
            num = " "
            mot = " "
            sco = " "
            embed = discord.Embed()

    return liste_embed

def top100(joueur,partie):
    top = [(joueur.top1000[i],
            round(partie.model.similarity(joueur.mot_mystere, joueur.top1000[i]) * 100, 2)) for i in range(99)]
    top.sort(key=lambda x: x[1])
    liste_embed = []
    i = 1
    score = ''
    mot = ''
    valide = ''
    embed = discord.Embed()
    for x in top:
        score = score + str(x[1]) + '\n'
        mot = mot + x[0] + '\n'
        if x[0] in joueur.essais:
            valide = valide + '\u2705' + '\n'
        else:
            valide = valide + '\u274C' + '\n'
        if i % 51 == 0 or x == top[-1]:
            embed.add_field(name='score', value=score, inline=True)
            embed.add_field(name='mot', value=mot, inline=True)
            embed.add_field(name='trouvé', value=valide, inline=True)
            liste_embed.append(embed)
            embed = discord.Embed()
            score = ''
            mot = ''
            valide = ''
        i += 1

    return liste_embed

def leaderboard():
    name = ""
    nb_vict = ""
    record = ""
    embed = discord.Embed(title="Classement",
                          description="Gagnez au moins une partie pour apparaitre dans le classement!",
                          colour= 0xf1c40f)
    winners = sauvegarde.get_lb()
    if not winners:
        return embed
    medals = ["\U0001f947  ","\U0001f948  ","\U0001f949  ", ""] #Or, Argent, Bronze, Rien
    compteur = 0
    for winner in winners:
        name = name + medals[compteur] + winner[0] + '\n'
        nb_vict = nb_vict + str(winner[1]) + '\n'
        record = record + winner[2] + '\n'
        if compteur < 4 :
            compteur+=1
    embed.add_field(name='Joueur', value=name, inline=True)
    embed.add_field(name='\U0001f3c6', value=nb_vict, inline=True)
    embed.add_field(name='Record', value=record, inline=True)
    return embed
