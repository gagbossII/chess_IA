import chess
import copy
import random

analyseCounter = 0 # Pour le test
analyseScore = -30
maxTurnSimulation = 4
materialScore = 0
board = chess.Board()
Hplayer = chess.WHITE # H pour humain
AIPlayer = chess.BLACK
moveSequence = []
FBestMoves = []
bestMovesCounter = 1
eatenPieces = []
alpha = float("-inf")
beta = float("inf")

def makeHMove() :
    movestr = str(input("Entrez un coup sous la forme suivante : a2a3. Dans cet exemple, a2 est la case de départ et a3 est la case d'arrivée."))
    return chess.Move.from_uci(movestr)

def getAvailableMoves():
    return board.generate_legal_moves() 

def playerOpposite(player):
    if player == Hplayer : return AIPlayer
    else: return Hplayer 

def bestMoveSequence(sequence, score):
    global FBestMoves
    global analyseScore
    for i in FBestMoves : 
        if i == sequence : return
    if score <= analyseScore :
        return
    elif len(FBestMoves) == 5 :
        FBestMoves.pop(4)
        FBestMoves.insert(0, copy.deepcopy(sequence))
        analyseScore = score
    else : 
        FBestMoves.insert(0, copy.deepcopy(sequence))
        analyseScore = score

def calcMaterialScore(pieces: list[chess.Piece], matScore: int):
    # Calcule le score de matériel pour chaque pièces prises. Adapté à la fois pour le jeu en général et pour les calculs de l'IA
    for piece in pieces:
        if piece.color == Hplayer :
            match piece.piece_type :
                case 1: matScore += 1
                case 2, 3: matScore += 3
                case 4: matScore += 5
                case 5: matScore += 9
                case _: continue
        if piece.color == AIPlayer :
            match piece.piece_type :
                case 1: matScore -= 1
                case 2, 3: matScore -= 3
                case 4: matScore -= 5
                case 5: matScore -= 9
                case _: continue
    return matScore

def scores(turn, matScore: int, player, checkRepetition, lastScore: int) : 
    score = 0
    # Calcule le score de l'IA lors de la fin de la parite simulé par celle-ci
    if board.is_game_over(claim_draw=True) and board.outcome() != None: 
        winner = board.outcome()
        match winner.termination :
            case 1, 8: score = 20 - (turn-1) - matScore # -matScore car le score de matériel est inversé par rapport au score de l'IA
            case 9: score = -20 + (turn-1) - matScore
            case _: score = 0
        if winner.winner == player : return -score # Inversion du score en cas de défaite de l'IA. Un score positif pour elle devient négatif avec la défaite
        else : return score
    # Calcule le score de l'IA dans le cas ou aucune solution de mat n'est trouvée mais qu'il y a un échec dnas le dernier coup simulé
    elif chess.BaseBoard.king(board, playerOpposite(player)) == None : return lastScore
    elif turn == maxTurnSimulation :
        if chess.BaseBoard.attackers(board, player, chess.BaseBoard.king(board, playerOpposite(player))) != None: # Analyse si la simulation se termine sur une situation d'échec 
            if player == Hplayer : score = lastScore - 5 - checkRepetition # Plus un échec est répeté, plus celui-ci rapporte de points
            else : score = lastScore + 5 + checkRepetition
        else : score = 0 + lastScore
    else : 
        if chess.BaseBoard.attackers(board, player, chess.BaseBoard.king(board, playerOpposite(player))) != None: # Analyse si la simulation se termine sur une situation d'échec 
            if player == Hplayer : score = lastScore - 2 - checkRepetition # Plus un échecs est répeté, plus celui-ci rapporte de points
            else : score = lastScore + 2 + checkRepetition
        else : score = 0 + lastScore
    return score


def alpha_beta(turn, matScore: int, player, checkHRepetition, checkAIRepetition, lastScore: int, moveSequence: list, takenPieces: list, a, b) :
    global bestMovesCounter
    global analyseScore
    global analyseCounter
    analyseCounter +=1
    if analyseCounter > 50000 : return True
    print("Score : " + str(analyseScore) + ", Count : " + str(analyseCounter)) # Pour tester
    # Permet de jouer directement une des 5 meilleures séquences sans devoir tout analyser à nouveau
    if turn == 0 and len(FBestMoves) > 1: # and bestMovesCounter < len(FBestMoves)
        for move in FBestMoves :
            if bestMovesCounter >= len(move): continue
            if board.peek() == move[bestMovesCounter] and bestMovesCounter < len(move)-1 :
                board.push(move[bestMovesCounter+1])
                print(board)
                bestMovesCounter += 2
                return
        bestMovesCounter = 1

    matScore = calcMaterialScore(takenPieces, matScore)
    if player == AIPlayer : 
        if board.checkers() == chess.SquareSet(chess.BB_EMPTY) : checkAIRepetition = 0
        else : checkAIRepetition += 1
        newScore = scores(turn, matScore, player, checkAIRepetition, lastScore)
    else : 
        if board.checkers() == chess.SquareSet(chess.BB_EMPTY) : checkHRepetition = 0
        else : checkHRepetition += 1
        newScore = scores(turn, matScore, player, checkHRepetition, lastScore)
    if board.is_game_over(claim_draw=True) or (turn == maxTurnSimulation):
        bestMoveSequence(moveSequence, newScore)
        return newScore

    if turn == maxTurnSimulation: 
        bestMoveSequence(moveSequence, newScore)
        return newScore
    else :
        if (turn * 2) % 2 != 0 :
            v = float("inf")
            for moves in getAvailableMoves() :
                if chess.BaseBoard.piece_at(board, moves.from_square) == None :
                    continue
                if chess.BaseBoard.piece_at(board, moves.from_square).color != board.turn :
                    continue
                if chess.BaseBoard.piece_at(board, moves.to_square) != None :
                    takenPieces.append(chess.BaseBoard.piece_at(board, moves.to_square))
                board.push(moves)
                moveSequence.append(moves)
                v = min(v, alpha_beta(turn+0.5, matScore, AIPlayer, checkHRepetition, checkAIRepetition, newScore, moveSequence, takenPieces, a, b))
                if a >= v : 
                    moveSequence.pop(len(moveSequence)-1)
                    board.pop()
                    return v
                b = min(b, v)
                moveSequence.pop(len(moveSequence)-1)
                board.pop()
        else :
            v = float("-inf")
            for moves in getAvailableMoves() :
                if chess.BaseBoard.piece_at(board, moves.from_square) == None :
                    continue
                if chess.BaseBoard.piece_at(board, moves.from_square).color != board.turn :
                    continue
                if chess.BaseBoard.piece_at(board, moves.to_square) != None :
                    takenPieces.append(chess.BaseBoard.piece_at(board, moves.to_square))
                board.push(moves)
                moveSequence.append(moves)
                v = max(v, alpha_beta(turn+0.5, matScore, Hplayer, checkHRepetition, checkAIRepetition, newScore, moveSequence, takenPieces, a, b))
                if b >= v : 
                    moveSequence.pop(len(moveSequence)-1)
                    board.pop()
                    return v
                a = max(a, v)
                moveSequence.pop(len(moveSequence)-1)
                board.pop()
    return v

    
def game() :
    global analyseScore
    global analyseCounter
    global alpha
    global beta
    print(board)
    for i in range(100):
        if board.is_game_over() : 
            print("Vous avez gagné.")
            exit(0)
        if i % 2 == 0 :
            move = makeHMove()
            if not(board.is_legal(move)) :
                print("Coup illégal. Vous avez perdu.")
                exit(0) # Idée de Mathurin Velas, membre honoraire de la table Pentagonale
            if chess.BaseBoard.piece_at(board, move.from_square).color != board.turn :
                print("Mauvaise couleur. Vous avez perdu.")
                exit(0) # Idée de Mathurin Velas, membre honoraire de la table Pentagonale
            if chess.BaseBoard.piece_at(board, move.to_square) != None :
                eatenPieces.append(chess.BaseBoard.piece_at(board, move.to_square))
            board.push(move)
            print(board)
        elif i: 
            rnd = random.choice(list(board.generate_legal_moves()))
            print(rnd)
            board.push(rnd)
            print(board)
        else : 
            analyseScore = -30
            analyseCounter = 0
            alpha = float("-inf")
            beta = float("inf")
            t = alpha_beta(0, calcMaterialScore(eatenPieces, 0), AIPlayer, 0, 0, analyseScore, [], [], alpha, beta)
            move = FBestMoves[0]
            print(move)
            print(board)
            print(t)
            board.push(move[0])
            print(board)
            
game()
