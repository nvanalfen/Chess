# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 18:01:49 2020

@author: nvana
"""
from enum import Enum
import numpy as np

# Enum class for representing the sides (White, Black)
# As well as the various pieces
class Pieces(Enum):
    White = 1
    Neutral = 0
    Black = -1
    
    WhitePawn = "WP"
    WhiteRook = "WR"
    WhiteKnight = "WH"
    WhiteKingBishop = "WKB"
    WhiteQueenBishop = "WQB"
    WhiteKing = "WK"
    WhiteQueen = "WQ"
    
    Blank = "X"
    
    BlackPawn = "BP"
    BlackRook = "BR"
    BlackKnight = "BH"
    BlackKingBishop = "BKB"
    BlackQueenBishop = "BQB"
    BlackKing = "BK"
    BlackQueen = "BQ"
    
    # Returns the color of a piece given
    def color(piece):
        if not isinstance(piece, Pieces) or piece == Pieces.Blank:
            return Pieces.Neutral
        if (piece == Pieces.WhitePawn) or (piece == Pieces.WhiteRook) \
            or (piece == Pieces.WhiteKnight) or (piece == Pieces.WhiteKingBishop) \
            or (piece == Pieces.WhiteQueenBishop) or (piece == Pieces.WhiteKing) \
            or (piece == Pieces.WhiteQueen):
                return Pieces.White
        return Pieces.Black
    
    def __eq__(self, other):
        return isinstance(other, Pieces) and self.value == other.value

# Class for representing the Chess board and functions for finding next possible moves
class Chess:
    dimension = 8
    
    def __init__(self):
        self.reset_grid()
    
    # Set up the starting grid
    def reset_grid(self):
        # Set up blanks
        self.grid = np.repeat(Pieces.Blank, Chess.dimension**2).reshape(Chess.dimension, Chess.dimension)
        
        # Fill in white pieces
        self.grid[0,0] = Pieces.WhiteRook
        self.grid[0,1] = Pieces.WhiteKnight
        self.grid[0,2] = Pieces.WhiteKingBishop
        self.grid[0,3] = Pieces.WhiteKing
        self.grid[0,4] = Pieces.WhiteQueen
        self.grid[0,5] = Pieces.WhiteQueenBishop
        self.grid[0,6] = Pieces.WhiteKnight
        self.grid[0,7] = Pieces.WhiteRook
        self.grid[1,:] = Pieces.WhitePawn
        
        # Fill in black pieces
        self.grid[7,0] = Pieces.BlackRook
        self.grid[7,1] = Pieces.BlackKnight
        self.grid[7,2] = Pieces.BlackKingBishop
        self.grid[7,3] = Pieces.BlackKing
        self.grid[7,4] = Pieces.BlackQueen
        self.grid[7,5] = Pieces.BlackQueenBishop
        self.grid[7,6] = Pieces.BlackKnight
        self.grid[7,7] = Pieces.BlackRook
        self.grid[6,:] = Pieces.BlackPawn
    
    def get_possible_moves(self, coord):
        pass
    
    # Returns all possible coordinates a rook at the given coordinate could go
    def rook_moves(self, coord):
        x,y = coord
        color = Pieces.color( self.grid[y,x] )
        coords = set()
        self.crawl_direction(x+1, y, 1, 0, coords, color)
        self.crawl_direction(x-1, y, -1, 0, coords, color)
        self.crawl_direction(x, y+1, 0, 1, coords, color)
        self.crawl_direction(x, y-1, 0, -1, coords, color)
        
        return coords
    
    def knight_move(self, coord):
        pass
    
    # Returns all possible coordinates a bishop at the given coordinate could go
    def bishop_move(self, coord):
        x,y = coord
        color = Pieces.color( self.grid[y,x] )
        coords = set()
        self.crawl_direction(x+1, y+1, 1, 1, coords, color)
        self.crawl_direction(x+1, y-1, 1, -1, coords, color)
        self.crawl_direction(x-1, y+1, -1, 1, coords, color)
        self.crawl_direction(x-1, y-1, -1, -1, coords, color)
        
        return coords
    
    def king_move(self, coord):
        pass
    
    # Returns all possible coordinates a queen at the given coordinate could go
    # Just the union of all rook and bishop moves
    def queen_move(self, coord):
        return ( self.rook_moves(coord) | self.bishop_move(coord) )
    
    def pawn_move(self, coord):
        pass
    
    # Checks to see if the current position puts either side in check
    def in_check(self, grid):
        pass
    
    # Checks to see if a coordinate is still on the grid
    def in_bounds(self, x, y):
        return x >= 0 and x < Chess.dimension and y >= 0 and y < Chess.dimension
    
    # Continues crawling in a given direction until a collision
    # Returns a set of all possible coordinates encountered
    def crawl_direction(self, x, y, dx, dy, coords, mover_color):
        # If we have left the grid or would hit one of our own pieces, it's not a valid move
        if not self.in_bounds(x,y) or mover_color == Pieces.color( self.grid[y,x] ):
            return
        
        coords.add( (x,y) )
        
        # If we haven't taken another piece, we can still move
        if self.grid[y,x] == Pieces.Blank:
            self.crawl_direction(x+dx, y+dy, dx, dy, coords, mover_color)
    
    # String representation of the chess board
    def __str__(self):
        return ",".join( [ el.value for el in self.grid.flatten() ] )
    
    def printable_grid(self):
        return np.array( (self.__str__()).split(",") ).reshape( (Chess.dimension, Chess.dimension) )