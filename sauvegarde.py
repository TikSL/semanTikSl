# Module permettant la sauvegarde des parties d'une journée à l'autre
# Création d'un leader board


def change_lb(playerName):
    lb_file = open("leaderboard.txt", 'r', encoding='utf-8')
    replacement = ""
    for line in lb_file :
        name, nbVict = line.split()
        nbrVict = int(nbVict)
        if name == playerName:
            change = line.replace(str(int(nbVict)), str(int(nbVict)+1))
        else :
            change = line
        replacement = replacement + change
    lb_file.close()

    lb_file = open("leaderboard.txt", "w", encoding='utf-8')
    lb_file.write(replacement)
    lb_file.close()


def get_lb():
    lb_file = open("leaderboard.txt", 'r', encoding='utf-8')
    winners = []
    for line in lb_file:
        name, nbVict = line.split()
        nbVict = int(nbVict)
        if nbVict > 0 :
            winners.append((name, nbVict))
    winners.sort(key=lambda x: x[1], reverse = True)
    return winners


def ajout_joueur_lb(joueur):
    lb_file = open("leaderboard.txt", 'r', encoding='utf-8')
    lines = lb_file.readlines()
    for line in lines:
        if joueur == line.split()[0]:
            return

    lines.append(joueur + " 0" + '\n')
    lb_file.close()
    lb_file = open("leaderboard.txt", "w", encoding='utf-8')
    for line in lines:
        lb_file.write(line)
    lb_file.close()




