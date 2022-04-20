import discord
from discord.ext import commands
from gensim.models import KeyedVectors
import random

commandes = ('!play', '!ff', '!stop', '!help', '!info', '!regles')

content = '**But du jeu :**\n' \
          'Trouver le mot mystère en donnant des mots à la suite.\n' \
          'Un score est attribué à chaque mot envoyé, les milles mots les plus proches sont mis en évidence.\n\n' \
          '\u26A0\uFE0F **Remarques :**\n' \
          'Dans un soucis de clarté, les mots accordés ont été retirés de la liste.\n' \
          'Vous ne cherchez donc qu\'un mot au masculin, au singulier ou non conjugué.\n\n' \
          '\U0001f6a7 **Bugs possibles :**\n' \
          '- Si le bot n\'arrive pas à calculer les 1000 mots les plus proches, il ne commencera pas la partie mais créera un salon. ' \
          'Dans ce cas revenez dans un salon textuel général (là ou vous avez tapé *!play*) et tapez *!stop*. ' \
          'Vous pouvez alors relancer une partie.\n' \
          '- Le joueur peut *!ff* même après une victoire.\n' \
          '- En théorie les accents comptent mais le dictionnaire utilisé est moyen.\n\n' \
          '\U0001f631 : mot le plus proche\n'\
          '\U0001f525 : top 10\n' \
          '\U0001f975 : top 100\n' \
          '\U0001f60e : top 1000\n' \
          '\U0001f976 : pas fou\n\n' \
          '\u2699\uFE0F **Commandes :**\n' \
          '!ff : abandonne pour voir le mot mystère\n' \
          '!stop : arrête la partie sans donner le mot mystère\n' \
          '!play : lance une partie\n' \
          '!help : pour plus d\'informations\n\n' \
          '	\U0001f340 Bonne chance ! \U0001f340'

embed_regles = discord.Embed(description=content, colour=0x2ecc71)

def infos(commande, utilisateur):
    print("------------------")
    print(utilisateur, commande)
    print("Joueur avec une partie en cours :")
    for joueur in jeu.en_jeu:
        print(joueur.name)
    print("Parties : ")
    for joueur in jeu.parties:
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


def get_dico():
    fichier = open(Semantiksl.dictionnaire, 'r', encoding='utf-8')
    lignes = fichier.readlines()
    liste = []
    for mot in lignes:
        liste.append(mot[:-1])
    fichier.close()
    return liste


def get_model():
    model = KeyedVectors.load_word2vec_format(Semantiksl.vecteurs, binary=True, unicode_errors="ignore")
    return model


def get_mot_mystere():
    fichier = open(Semantiksl.dictionnaire_mot_mystere, 'r', encoding='utf-8')
    mots = fichier.readlines()
    n = len(mots)
    rd = random.randint(0, n - 1)
    mm = mots[rd][:-1]
    fichier.close()
    return mm


def position_top1000(mot, joueur):
    if mot in joueur.top1000:
        return 999 - joueur.top1000.index(mot)
    else:
        return -1


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


def top100(joueur):
    top = [(joueur.top1000[i], round(jeu.model.similarity(joueur.mot_mystere, joueur.top1000[i]) * 100, 2)) for i in range(99)]
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
        if x[0] in joueur.teste:
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


class Semantiksl:
    dictionnaire = "dico_ms.txt"
    dictionnaire_mot_mystere = "dico_mm.txt"
    vecteurs = "frWac_non_lem_no_postag_no_phrase_200_cbow_cut100.bin"

    def __init__(self):
        self.en_jeu = []
        self.parties = []
        self.dico = get_dico()
        self.model = get_model()

    def get_salon(self, name):
        for joueur in self.parties:
            if joueur.name == name:
                return joueur.salon
        return

    def get_joueur(self, name):
        for joueur in self.parties:
            if joueur.name == name:
                return joueur
        return

    async def nouveau_joueur(self, name, salon):
        joueur = Joueur(name, salon)
        joueur.top1000 = self.get_top1000(joueur)
        self.parties.append(joueur)
        self.en_jeu.append(name)
        await salon.send(embed=embed_regles)
        return

    def enlever_joueur(self, name):
        for joueur in self.parties:
            if joueur.name == name:
                self.en_jeu.remove(name)
        joueur = self.get_joueur(name)
        self.parties.remove(joueur)
        return

    def get_top1000(self, joueur):
        top_potentiel = self.model.most_similar(joueur.mot_mystere, topn=10000)
        top_mille = ['_' for _ in range(999)]
        i = 0
        k = 0
        while top_mille[998] == '_':
            if top_potentiel[i][0] in self.dico:
                top_mille[k] = top_potentiel[i][0]
                k += 1
            if i == 10000:
                print("ATTENTION LA LISTE DES MILLES MOTS N'A PAS PU ETRE CONSTRUITE ENTIEREMENT. TOP : %d" % k)
                break
            i += 1
        return top_mille

    async def essais(self, mot, joueur):

        salon = joueur.salon
        if len(joueur.essais) > 0:
            liste_essais = liste_discord(joueur.essais)
            for embed in liste_essais:
                await salon.send(embed=embed)

        try:

            if mot == joueur.mot_mystere:
                joueur.victoire = True
                for embed in top100(joueur):
                    await salon.send(embed=embed)
                await salon.send("\U0001f973 C'est gagné ! \U0001f973")
                await salon.send("Le mot était bien : " + joueur.mot_mystere)
                await salon.send("Vous l'avez trouvé en " + str(joueur.nbr_essais + 1) + " essais.")
                overwrites = {
                    discord.Guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    joueur.name: discord.PermissionOverwrite(send_messages=False, read_messages=True),
                }
                await salon.edit(overwrites=overwrites)
                return

            if mot in joueur.teste:
                await salon.send("\u267B Vous avez déjà donné ce mot ! \u267B")
                return

            if mot in jeu.dico:
                score = round(self.model.similarity(joueur.mot_mystere, mot) * 100, 2)
            else:
                raise KeyError

            position = position_top1000(mot, joueur)
            joueur.nbr_essais += 1

            affiche_position = ''
            if position != -1:
                affiche_position = str(position) + '/1000'

            await salon.send(
                'Essai n° ' + str(joueur.nbr_essais) + ' :   ' + mot + '    ' + affiche_position + '   ' + emoji(
                    position) + '    | Score = ' + str(score))
            joueur.essais.append((joueur.nbr_essais, mot, score, position, emoji(position)))
            joueur.teste.append(mot)
            joueur.trier_essais()

        except KeyError:
            await salon.send("\u26D4 Mot invalide \u26D4")


class Joueur:

    def __init__(self, name, salon):
        self.name = name
        self.nbr_essais = 0
        self.essais = []
        self.salon = salon
        self.teste = []
        self.mot_mystere = get_mot_mystere()
        self.top1000 = []

    def trier_essais(self):
        self.essais.sort(key=lambda x: x[2])
        return


bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print("Le bot est prêt !")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content not in commandes:
        if len(jeu.en_jeu) > 0:
            name = message.author
            if name in jeu.en_jeu:
                joueur = jeu.get_joueur(name)
                if message.channel == joueur.salon:
                    mot = message.content
                    compteur = 0
                    async for _ in message.channel.history(limit=None):
                        compteur += 1
                    await message.channel.purge(limit=compteur - 1)
                    await jeu.essais(mot.lower(), joueur,)
    await bot.process_commands(message)


@bot.command()
async def play(ctx):
    """
    Créé une nouvelle partie avec le salon associé
    Seul le joueur (et les administrateurs) ont accés à ce salon

    Si le joueur a déjà une partie en cours alors un message d'erreur s'affiche
    """
    joueur = ctx.message.author
    if joueur in jeu.en_jeu:
        salon = jeu.get_salon(joueur)
        await ctx.send(joueur.mention + "Vous avez déjà une partie en cours :" + salon.mention + '\nTapez *!stop* si vous voulez la supprimer.')
        infos('!play echec', ctx.message.author)
    else:
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            bot.user: discord.PermissionOverwrite(read_messages=True),
            joueur: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await ctx.guild.create_text_channel('Partie de ' + joueur.display_name, overwrites=overwrites)
        await ctx.send(joueur.mention + " Partie créée :  " + channel.mention)
        await jeu.nouveau_joueur(joueur, channel)
        infos('!play succes', ctx.message.author)


@bot.command()
async def ff(ctx):
    """
    Abandonne la partie
    Le mot est affiché sous spoiler dans le salon de la partie
    Le joueur ne peut plus écrire dans ce salon
    """
    nom_joueur = ctx.message.author
    if nom_joueur in jeu.en_jeu:
        salon = jeu.get_salon(nom_joueur)
        joueur = jeu.get_joueur(nom_joueur)

        for embed in top100(joueur):
            await salon.send(embed=embed)

        await salon.send("Terrible \U0001f622 le mot mystère était : ||" + joueur.mot_mystere + "||")
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            nom_joueur: discord.PermissionOverwrite(send_messages=False, read_messages=True),
        }
        await salon.edit(overwrites=overwrites)
        infos('!ff succes', ctx.message.author)
    else:
        await ctx.send(nom_joueur.mention + ' vous n\'avez aucune partie en cours.')
        infos('!ff echec', ctx.message.author)


@bot.command()
async def stop(ctx):
    """
    Ferme le salon de la partie du joueur
    Si le joueur n'a pas de partie en cours alors un message d'erreur s'affiche
    """
    joueur = ctx.message.author
    if joueur in jeu.en_jeu:
        salon = jeu.get_salon(joueur)
        jeu.enlever_joueur(joueur)
        await ctx.send(joueur.mention + ' votre partie est supprimée.')
        await salon.delete()
        infos('!stop succes', ctx.message.author)
    else:
        await ctx.send(joueur.mention + ' vous n\'avez aucune partie en cours.')
        infos('!stop echec', ctx.message.author)


@bot.command()
async def info(ctx):
    """
    Commande pour les admins. Ne pas spammer
    """
    infos('!info', ctx.message.author)


@bot.command()
async def regles(ctx):
    """
    Affiche les règles et des indications
    """
    await ctx.send(ctx.author.mention, embed=embed_regles)
    infos('!regles', ctx.message.author)


jeu = Semantiksl()

print("Les dictionnaires sont chargés")

bot.run("Token du bot")
