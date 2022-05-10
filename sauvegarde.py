# Création d'un leader board
# Note les heures de début de partie avec les id des salons correspondant


def change_lb(playerName, essais):
    lb_file = open("leaderboard.txt", 'r', encoding='utf-8')
    replacement = ""
    for line in lb_file :
        name, nbVict, record = line.split()
        record = int(record)
        if name == playerName or record > essais :
            change = line.replace(name + ' ' + str(int(nbVict)) + ' ' + str(record),
                                  name + ' ' + str(int(nbVict)+1) + ' ' + str(essais))
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
        name, nbVict, record = line.split()
        nbVict = int(nbVict)
        if nbVict > 0 :
            winners.append((name, nbVict, record))
    winners.sort(key=lambda x: x[1], reverse = True)
    lb_file.close()
    return winners


def ajout_joueur_lb(joueur):
    lb_file = open("leaderboard.txt", 'r', encoding='utf-8')
    lines = lb_file.readlines()
    for line in lines:
        if joueur == line.split()[0]:
            return

    lines.append(joueur + " 0" + " 10000" + '\n')
    lb_file.close()
    lb_file = open("leaderboard.txt", "w", encoding='utf-8')
    for line in lines:
        lb_file.write(line)
    lb_file.close()






