import chess

maxTurnSimulation = 4
materialScore = 0
board = chess.Board()
Hplayer = chess.WHITE # H pour humain
AIPlayer = chess.BLACK
FBestMoves = []
eatenPieces = []

def getAvailableMoves():
    avMoves = board.generate_legal_moves() 

def playerOpposite(player):
    if player == Hplayer : return AIPlayer
    else: return Hplayer 

def calcMaterialScore(pieces: list[chess.Piece], matScore):
    # Calcule le score de matériel pour chaque pièces prises. Adapté à la fois pour le jeu en général et pour les calculs de l'IA
    for piece in pieces:
        if piece.color == Hplayer :
            match piece.piece_type:
                case 1: matScore += 1
                case 2, 3: matScore += 3
                case 4: matScore += 5
                case 5: matScore += 9
                case _: continue
        if piece.color == AIPlayer :
            match piece.piece_type:
                case 1: matScore -= 1
                case 2, 3: matScore -= 3
                case 4: matScore -= 5
                case 5: matScore -= 9
                case _: continue
    return matScore

def scores(turn, matScore, player, checkRepetition, lastScore) : 
    score = 0
    # Calcule le score de l'IA lors de la fin de la parite simulé par celle-ci
    if board.is_game_over(claim_draw=True): 
        winner = board.outcome()
        match winner.termination :
            case 1, 8: score = 20 - (turn-1) - matScore # -matScore car le score de matériel est inversé par rapport au score de l'IA
            case 9: score = -20 + (turn-1) - matScore
            case _: score = 0
        if winner.winner == player : return -score # Inversion du score en cas de défaite de l'IA. Un score positif pour elle devient négatif avec la défaite
        else : return score
    # Calcule le score de l'IA dans le cas ou aucune solution de mat n'est trouvée mais qu'il y a un échec dnas le dernier coup simulé
    elif turn == maxTurnSimulation :
        if chess.BaseBoard.attackers(player, chess.BaseBoard.king(playerOpposite(player))) != None: # Analyse si la simulation se termine sur une situation d'échec 
            if player == Hplayer : score = lastScore - 5 - checkRepetition # Plus un échec est répeté, plus celui-ci rapporte de points
            else : score = lastScore + 5 + checkRepetition
        else : score = 0
    else : 
        if chess.BaseBoard.attackers(player, chess.BaseBoard.king(playerOpposite(player))) != None: # Analyse si la simulation se termine sur une situation d'échec 
            if player == Hplayer : score = -2 - checkRepetition # Plus un échecs est répeter, plus celui-ci rapporte ed points
            else : score = 2 + checkRepetition
        else : score = 0



def minimax():
    pass
        