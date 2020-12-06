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
        board.replace( np.random.choice(children) )
        current.append( board.check( board, Pieces.Black ) )
        current.append( board.checkmate( Pieces.Black ) )
        current.append( board.copy() )
        
        if current[-2]:
            results.append( current )
            break
        
        children = board.generate_valid_children(Pieces.Black)
        board.replace( np.random.choice(children) )
        current.append( board.check( board, Pieces.White ) )
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

board = Chess()
board, results, duration = test(board)