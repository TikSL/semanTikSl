import discord
from discord.ext import commands

import dico
import affichage
import sauvegarde


def position_top1000(mot, joueur):
    if mot in joueur.top1000:
        return 999 - joueur.top1000.index(mot)
    else:
        return -1


class Semantiksl:
    dictionnaire = "dico_ms.txt"
    dictionnaire_mot_mystere = "dico_mm.txt"
    vecteurs = "frWac_non_lem_no_postag_no_phrase_200_cbow_cut100.bin"

    def __init__(self):
        self.en_jeu = []
        self.parties = []
        self.dico = dico.get_dico(self.dictionnaire)
        self.model = dico.get_modele(self.vecteurs)

    def get_joueur(self, name):
        for joueur in self.parties:
            if joueur.name == name:
                return joueur
        return

    async def nouveau_joueur(self, nom_joueur, salon):
        joueur = Joueur(nom_joueur, salon)
        joueur.top1000 = self.get_top1000(joueur)
        self.parties.append(joueur)
        self.en_jeu.append(joueur.name)
        sauvegarde.ajout_joueur_lb(joueur.name.name)
        await salon.send(embed=affichage.embed_regles)
        return joueur

    def enlever_joueur(self, joueur):
        self.en_jeu.remove(joueur.name)
        self.parties.remove(joueur)
        return

    def get_top1000(self, joueur):
        top_potentiel = self.model.most_similar(joueur.mot_mystere, topn=10000)
        top_mille = ['_' for _ in range(999)]
        i = 0
        k = 0
        while top_mille[998] == '_':
            try:
                if top_potentiel[i][0] in self.dico and i < 10000:
                    top_mille[k] = top_potentiel[i][0]
                    k += 1
                i += 1
            except:
                print("Erreur avec le mot mystère : ", joueur.mot_mystere)
                joueur.mot_mystere = dico.get_mot_mystere(jeu)
                return self.get_top1000(joueur)
        return top_mille

    async def essais(self, mot, joueur):

        if len(joueur.essais_eval) > 0:
            liste_essais = affichage.liste_discord(joueur.essais_eval)
            for embed in liste_essais:
                await joueur.salon.send(embed=embed)
        try:
            if mot == joueur.mot_mystere:
                joueur.fini = True
                sauvegarde.change_lb(joueur.name.name, joueur.nbr_essais + 1)
                for embed in affichage.top100(joueur, jeu):
                    await joueur.salon.send(embed=embed)
                await joueur.salon.send(
                    '\U0001f973 C\'est gagné ! \U0001f973 \n'
                    'Le mot était bien : ' + joueur.mot_mystere + '\n'
                    'Vous l\'avez trouvé en ' + str(joueur.nbr_essais + 1) + ' essais.')
                overwrites = {
                    discord.Guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    joueur.name: discord.PermissionOverwrite(send_messages=False, read_messages=True)
                }
                await joueur.salon.edit(overwrite=overwrites)

                return

            if mot in joueur.essais:
                await joueur.salon.send("\u267B Vous avez déjà donné ce mot ! \u267B")
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

            await joueur.salon.send(
                'Essai n° ' + str(joueur.nbr_essais) + ' :   ' + mot + '    ' + affiche_position + '   ' +
                affichage.emoji(position) + '    | Score = ' + str(score))
            joueur.essais_eval.append((joueur.nbr_essais, mot, score, position, affichage.emoji(position)))
            joueur.essais.append(mot)
            joueur.trier_essais()

        except KeyError:
            await joueur.salon.send("\u26D4 Mot invalide : " + mot + "\u26D4")


class Joueur:

    def __init__(self, name, salon):
        self.name = name  # exemple: pseudo#0000
        self.salon = salon
        self.nbr_essais = 0
        self.essais_eval = []
        self.essais = []
        self.mot_mystere = dico.get_mot_mystere(jeu)
        self.top1000 = []
        self.fini = False

    def trier_essais(self):
        self.essais_eval.sort(key=lambda x: x[2])  # essai_eval???
        return


bot = commands.Bot(command_prefix="$")


@bot.event
async def on_ready():
    print("Le bot est prêt !")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print("------------------")


@bot.event
async def on_message(message):
    """
    Lis tous les messages.
    Repère ceux qui viennent d'un joueur en jeu et évalue le mot.
    Supprime ensuite la file de message du salon.
    """
    pseudo = message.author
    if pseudo == bot.user:
        return
    if message.content not in affichage.commandes:
        if pseudo in jeu.en_jeu:
            joueur = jeu.get_joueur(pseudo)
            if message.channel == joueur.salon:
                mot = message.content.lower()
                compteur = 0
                async for _ in message.channel.history(limit=None):
                    compteur += 1
                await message.channel.purge(limit=compteur - 1)
                await jeu.essais(mot, joueur)
    await bot.process_commands(message)
    return


@bot.command()
async def play(ctx, mode="solo"):
    """
    Créé une nouvelle partie avec le salon associé.
    Seul le joueur (et les administrateurs) ont accès à ce salon.
    Si le joueur a déjà une partie en cours alors un message d'erreur s'affiche.
    """
    pseudo = ctx.message.author
    if pseudo in jeu.en_jeu:  # Vérifie si le joueur joue déjà une partie
        joueur = jeu.get_joueur(pseudo)
        await ctx.send(joueur.name.mention + "Vous avez déjà une partie en cours :" + joueur.salon.mention +
                       '\nTapez *$stop* si vous voulez la supprimer.')
        affichage.infos(jeu, '$play echec', joueur.name)
    else:
        category = ctx.message.channel.category
        print(category)
        if mode == 'multi':
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False, read_messages=True),
                bot.user: discord.PermissionOverwrite(read_messages=True),
                pseudo: discord.PermissionOverwrite(read_messages=True)
            }
            salon = await ctx.guild.create_text_channel('Partie de ' + pseudo.display_name + " (multi)",
                                                        category=category,
                                                        overwrites=overwrites)
        elif mode == 'solo':
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                bot.user: discord.PermissionOverwrite(read_messages=True),
                pseudo: discord.PermissionOverwrite(read_messages=True)
            }
            salon = await ctx.guild.create_text_channel('Partie de ' + pseudo.display_name, category=category,
                                                        overwrites=overwrites)
        else:
            await ctx.send(pseudo.mention + " Erreur de commande : $play ou $play multi")
            return
        joueur = await jeu.nouveau_joueur(pseudo, salon)
        await ctx.send(joueur.name.mention + " Partie créée :  " + joueur.salon.mention)
        affichage.infos(jeu, '!play succes', pseudo)
    pass


@bot.command()
async def ff(ctx):
    """
    Abandonne la partie
    Le mot est affiché sous spoiler dans le salon de la partie
    Le joueur ne peut plus écrire dans ce salon
    """
    pseudo = ctx.message.author
    if pseudo in jeu.en_jeu:
        joueur = jeu.get_joueur(pseudo)
    else:
        await ctx.send(pseudo.mention + ' vous n\'avez aucune partie en cours.')
        affichage.infos(jeu, '!ff echec', pseudo)
        return
    if not joueur.fini:
        for embed in affichage.top100(joueur, jeu):
            await joueur.salon.send(embed=embed)
        await joueur.salon.send("Terrible \U0001f622 le mot mystère était : ||" + joueur.mot_mystere + "||")

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            joueur.name: discord.PermissionOverwrite(send_messages=False, read_messages=True),
        }
        await joueur.salon.edit(overwrite=overwrites)
        affichage.infos(jeu, '!ff succes', pseudo)
        joueur.fini = True
    else:
        await ctx.send(pseudo.mention + ' vous n\'avez aucune partie en cours.')
        affichage.infos(jeu, '!ff echec', pseudo)
    return


@bot.command()
async def stop(ctx):
    """
    Ferme le salon de la partie du joueur
    Si le joueur n'a pas de partie en cours alors un message d'erreur s'affiche
    """
    pseudo = ctx.message.author
    if pseudo in jeu.en_jeu:
        joueur = jeu.get_joueur(pseudo)
        await ctx.send(pseudo.mention + ' votre partie est supprimée.')
        await joueur.salon.delete()
        jeu.enlever_joueur(joueur)
        affichage.infos(jeu, '!stop succes', pseudo)
    else:
        await ctx.send(pseudo.mention + ' vous n\'avez aucune partie en cours.')
        affichage.infos(jeu, '!stop echec', pseudo)
    pass


@bot.command()
async def regles(ctx):
    """
    Affiche les règles et des indications
    """
    await ctx.send(ctx.author.mention, embed=affichage.embed_regles)
    affichage.infos(jeu, '!regles', ctx.message.author)
    pass


@bot.command()
async def classement(ctx):
    """Affiche les joueurs ayant gagné une partie"""
    await ctx.send(embed=affichage.leaderboard())
    pass


@commands.has_permissions(administrator=True)
@bot.command()
async def info(ctx):
    """
    Commande pour les admins. Ne pas spammer
    """
    affichage.infos(jeu, '!info', ctx.message.author)
    pass


@commands.has_permissions(administrator=True)
@bot.command()
async def dl(ctx, nom_fichier):
    """
    Commande pour les admins. Ne pas spammer
    """
    fichier = nom_fichier + '.txt'
    await ctx.send(file=discord.File(fichier))
    pass


jeu = Semantiksl()

print("Les dictionnaires sont chargés")

bot.run(" ")
