import math

table = [" " for i in range(9)]
player1 = "X"
aiPlayer = "O"

def writeTable() : 
    for i in range(0, 9, 3) : 
        print(f"{table[i]} | {table[i+1]} | {table[i+2]}")
        if i < 6 :
            print("---------")

def writeInTable(player, index) : 
    if table[index] != " " : return
    table[index] = player 
    writeTable()

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
    writeTable()
    for i in range(9) :
        if i % 2 == 0 :
            writeInTable(player1, play(i))
        else :
            writeInTable(aiPlayer, get_best_move())
        if getWinner() == None :
            continue
        else : 
            print(f"Le gagnant est {getWinner()}")
            return

def minimax(recurs, player) :
    winner = getWinner()
    if winner == aiPlayer :
        return 1
    if winner == player1 :
        return -1
    if " " not in table :
        return 0
    if player == aiPlayer :
        best = float("-inf")
        for i in range(len(table)) :
            if table[i] != " " : continue
            table[i] = aiPlayer 
            score = minimax(recurs + 1, player1)
            table[i] = " "
            best = max(score, best)
        return best
    else :
        best = float("+inf")
        for i in range(len(table)) :
            if table[i] != " " : continue
            table[i] = player1 
            score = minimax(recurs + 1, aiPlayer)
            table[i] = " "
            best = min(score, best)
        return best
    
def get_best_move():
    best_score = float("-inf") 
    best_move = None 
    for i in range(len(table)): 
        if table[i] != " " : continue
        table[i] = aiPlayer 
        score = minimax(0, aiPlayer)
        print(score)
        table[i] = " " 
        if score >= best_score: 
            best_score = score 
            best_move = i 
    return best_move

game()