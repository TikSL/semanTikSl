# Création d'un leader board
# Note les heures de début de partie avec les id des salons correspondant


def change_lb(player_name, essais):
    lb_file = open("leaderboard.txt", 'r', encoding='utf-8')
    replacement = ""
    for line in lb_file:
        name, nbr_victoires, record = line.split()
        record = int(record)
        if name == player_name:
            if record > essais:
                change = line.replace(name + ' ' + str(int(nbr_victoires)) + ' ' + str(record),
                                      name + ' ' + str(int(nbr_victoires)+1) + ' ' + str(essais))
            else:
                change = line.replace(name + ' ' + str(int(nbr_victoires)) + ' ' + str(record),
                                      name + ' ' + str(int(nbr_victoires) + 1) + ' ' + str(record))
        else:
            change = line
        replacement = replacement + change
    lb_file.close()

    lb_file = open("leaderboard.txt", "w", encoding='utf-8')
    lb_file.write(replacement)
    lb_file.close()


def get_lb():
    lb_file = open("leaderboard.txt", 'r', encoding='utf-8')
    winners = []
    lines = lb_file.readlines()
    for line in lines:
        name, nbr_victoires, record = line.split()
        nbr_victoires = int(nbr_victoires)
        if nbr_victoires > 0:
            winners.append((name, nbr_victoires, record))
    winners.sort(key=lambda x: x[1], reverse=True)
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
