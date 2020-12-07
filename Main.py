# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:54:41 2020

@author: nvana
"""

from Chess import Pieces, Chess
import time
import numpy as np

def test(board):
    start = time.time()
    
    results = []
    prev_count = 32
    current_count = 32
    captureless = 0
    
    while True:
        
        prev_count = current_count
        
        current = []
        
        children = board.generate_valid_children(Pieces.White)
        board.replace( children[np.random.choice( np.arange(len(children)) )] )
        current.append( board.check( board.grid, Pieces.Black ) )
        current.append( board.checkmate( Pieces.Black ) )
        current.append( board.copy() )
        
        if current[-2]:
            results.append( current )
            break
        
        children = board.generate_valid_children(Pieces.Black)
        board.replace( children[np.random.choice( np.arange(len(children)) )] )
        current.append( board.check( board.grid, Pieces.White ) )
        current.append( board.checkmate( Pieces.White ) )
        current.append( board.copy() )
        
        results.append( current )
        
        if current[-2]:
            break
        
        current_count = board.count_pieces()
        if current_count == prev_count:
            captureless += 1
        else:
            captureless = 0
        if captureless == 50:
            break
    
    return board, results, (time.time()-start)

games = 10

for i in range(games):
    print("\nGame: ",i)
    board = Chess()
    board, results, duration = test(board)
    #stuff = test(board)
    if board.checkmate(Pieces.White):
        print("Black has won")
    elif board.checkmate(Pieces.Black):
        print("White has won")
    else:
        print("Tie...")
    print(len(results)," rounds")
