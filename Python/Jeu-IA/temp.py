def minimax(turn, matScore: int, player, checkHRepetition, checkAIRepetition, lastScore: int, moveSequence: list, takenPieces: list):
    global bestMovesCounter
    global analyseScore
    global analyseCounter
    analyseCounter +=1
    if analyseCounter > 15000 : return True
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
    
    #Initialisation des variables récursives et analyse des coups. Cette partie retourne à la fois un score et une séquence de coups
    matScore = calcMaterialScore(takenPieces, matScore)
    if player == AIPlayer : 
        if board.checkers() == None : checkAIRepetition = 0
        else : checkAIRepetition += 1
        newScore = scores(turn, matScore, player, checkAIRepetition, lastScore)
    else : 
        if board.checkers() == None : checkHRepetition = 0
        else : checkHRepetition += 1
        newScore = scores(turn, matScore, player, checkHRepetition, lastScore)
    if board.is_game_over(claim_draw=True) or (turn == maxTurnSimulation):
        bestMoveSequence(moveSequence, newScore)
        return newScore   
    
    # Mise en place de la récursivité
    if board.turn == Hplayer : 
        for moves in getAvailableMoves() :
            if chess.BaseBoard.piece_at(board, moves.from_square).color != board.turn :
                continue
            if chess.BaseBoard.piece_at(board, moves.to_square) != None :
                takenPieces.append(chess.BaseBoard.piece_at(board, moves.to_square))
            board.push(moves)
            moveSequence.append(moves)
            minimax(turn+0.5, matScore, AIPlayer, checkHRepetition, checkAIRepetition, newScore, moveSequence, takenPieces) # +0.5 car on compte les tour de l'IA et du joueur donc pour analyser le nombre de coups spécifiés par maxTurnSimulation, il faut diviser par 2
            moveSequence.pop(len(moveSequence)-1)
            board.pop()
        return True
    if board.turn == AIPlayer : 
        for moves in getAvailableMoves() :
            if chess.BaseBoard.piece_at(board, moves.from_square).color != board.turn :
                continue
            if chess.BaseBoard.piece_at(board, moves.to_square) != None :
                takenPieces.append(chess.BaseBoard.piece_at(board, moves.to_square))
            board.push(moves)
            moveSequence.append(moves)
            minimax(turn+0.5, matScore, Hplayer, checkHRepetition, checkAIRepetition, newScore, moveSequence, takenPieces) # +0.5 car on compte les tour de l'IA et du joueur donc pour analyser le nombre de coups spécifiés par maxTurnSimulation, il faut diviser par 2
            moveSequence.pop(len(moveSequence)-1)
            board.pop()
        return True