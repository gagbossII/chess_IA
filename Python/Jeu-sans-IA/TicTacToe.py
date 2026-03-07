table = [" " for i in range(9)]
player1 = "X"
player2 = "O"

def writeTable() : 
    for i in range(0, 9, 3) : 
        print(f"{table[i]} | {table[i+1]} | {table[i+2]}")
        if i < 6 :
            print("---------")

def writeInTable(player, index) : 
    if table[index] != " " : return
    table[index] = player 
    writeTable()

def winner() :
    for i in range(0, 9, 3) :
        if table[i] == table[i+1] == table[i+2] != " ": return table[i]
    for i in range(0, 3) :
        if table[i] == table[i+3] == table[i+6] != " ": return table[i]
    if table[4] == " " : return None
    elif table[0] == table[4] == table[8] or table[2] == table[4] == table[6] :
        return table[4]
    else : return None

def play(turn) : 
    if turn % 2 == 0 :
        return int(input("Joueur 1, donnez le numéro de la case où vous voulez jouer : "))
    else :
        return int(input("Joueur 2, donnez le numéro de la case où vous voulez jouer : ")) 

def game() : 
    writeTable()
    for i in range(9) :
        if i % 2 == 0 :
            writeInTable(player1, play(i))
        else :
            writeInTable(player2, play(i))
        if winner() == None :
            continue
        else : 
            print(f"Le gagnant est {winner()}")
            return

game()