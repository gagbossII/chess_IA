import math

table = [" " for i in range(9)]
player1 = "X"
aiPlayer = "O"
bestMove = 0
bestscore = -10

def writeTable() : 
    for i in range(0, 9, 3) : 
        # Ecrit ligne par ligne le tableau
        print(f"{table[i]} | {table[i+1]} | {table[i+2]}")
        if i < 6 :
            print("---------")
    print("\n")

def writeInTable(player, index) : 
    if table[index] != " " : return
    table[index] = player 
    writeTable()

def availablesMoves() :
    return [i for i, spot in enumerate(table) if spot == " "]

def getWinner() :
    for i in range(0, 9, 3) :
        if table[i] == table[i+1] == table[i+2] != " ": return table[i]
    for i in range(0, 3) :
        if table[i] == table[i+3] == table[i+6] != " ": return table[i]
    if table[4] == " " : return None
    elif table[0] == table[4] == table[8] or table[2] == table[4] == table[6] :
        return table[4]
    else : return None

def play(turn) : 
    return int(input("Joueur 1, donnez le numéro de la case où vous voulez jouer : "))

def game() : 
    global bestscore
    writeTable()
    for i in range(12) : # Dans le cas où un joueur fait une erreur et doit rejouer une fois de plus
        if availablesMoves() == [] : print("Egalité")
        if i % 2 == 0 : # Permet de faire jouer l'un après l'autre les joueurs. Tour du joueur.
            writeInTable(player1, play(i))
        else : # Tour de l'IA
            writeInTable(aiPlayer, minimax(0, aiPlayer, availablesMoves()[0]))
            bestscore = -10
        if getWinner() == None : # Si il n'y a pas de vainqueur
            continue
        else : 
            print(f"Le gagnant est {getWinner()}")
            return

def minimax(turn, player, move) :
    global bestscore
    global bestMove
    # Défini les scores minimaux et maximaux pour le tour. On fait ça car plus il y faut de tour pour gagner, moins le coup est bon.
    scoreMin = -1 + turn/8 
    scoreMax = 1 - turn/8 
    # Donne les scores en fonction d'une victoire, une défaite ou d'un nul et retourne le coup qui a permis d'arriver à ce résultat
    if (turn == 2 and getWinner() == player1 and bestscore < 1) :
        bestscore = 1
        return move
    if (turn == 1 and getWinner() == aiPlayer) :
        bestscore = 2
        return move
    if (getWinner() == player1) :
        if bestscore < scoreMin : 
            bestscore = scoreMin
            return move
    if (getWinner() == aiPlayer) :
        if bestscore < scoreMax : 
            bestscore = scoreMax
            return move
    if (" " not in table) :
        if bestscore < 0 :
            bestscore = 0 
            return move
    # Mise en place de la récursivité pour permettre à l'algorithme de voir tout les coups possibles 
    
    if player == aiPlayer :
        for moves in availablesMoves() :
            table[moves] = aiPlayer
            bestMove = minimax(turn+1, player1, moves)
            table[moves] = " "
        return bestMove
    else :
        for moves in availablesMoves() :
            table[moves] = player1
            bestMove = minimax(turn+1, aiPlayer, moves)
            table[moves] = " "
        return bestMove

game()
        