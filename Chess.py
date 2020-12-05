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
    
    def enemy_color(color):
        if color == Pieces.White:
            return Pieces.Black
        if color == Pieces.Black:
            return Pieces.White
    
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
    
    # Move the piece at the source coordinate to the target coordinate
    # Parameters:
    #   source      ->  2-tuple of (x,y) coordinate for the piece being moved
    #   target      ->  2-tuple of (x,y) coordinate for the location the piece is being moved to
    def move(self, source, target):
        x1, y1 = source
        x2, y2 = target
        
        self.grid[y2,x2] = self.grid[y1,x1]             # Move the piece to the new location
        self.grid[y1,x1] = Pieces.Blank                 # Replace the old location with a blank
    
    # Generates all possible grids that can be reached in one move from the current grid
    # Parameters:
    #   turn        ->  Pieces.Black or Pieces.White, whoever's turn it is to move
    # Returns:
    #   children    ->  list of numpy arrays representing the grid configuration
    def generate_children(self, turn):
        transitions = self.generate_transitions(turn)
        children = []
        for source, target in transitions:
            child = self.copy()
            child.move(source, target)
            children.append( child )
        
        return children
    
    # Generates all start to end transitions that can be made from the current grid
    # Parameters:
    #   turn        ->  Pieces.Black or Pieces.White, whoever's turn it is to move
    # Returns:
    #   transitions ->  list of 2-tuples where each element is a 2-tuple representing an (x,y) coordinate
    #                   the first 2-tuple is the start point, the second is the end point
    def generate_transitions(self, turn):
        sources = set()
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if Pieces.color( self.grid[y,x] ) == turn:
                    sources.add( (x,y) )
        
        transitions = []
        for source in sources:
            targets = self.get_possible_moves(source)
            for target in targets:
                transitions.append( (source, target) )
        
        return transitions
    
    # Given a coordinate, decide which type of piece it is and return moves appropriate for that
    # Parameters:
    #   coord       ->  2-tuple of (x,y) coordinate where the piece in question is located
    # Returns:
    #   coords      ->  set of 2-tuples of (x,y) coordinates where the piece in question could move
    def get_possible_moves(self, coord):
        x,y = coord
        piece = self.grid[y,x]
        
        if piece == Pieces.WhitePawn or piece == Pieces.BlackPawn:
            return self.pawn_move(coord)
        if piece == Pieces.WhiteRook or piece == Pieces.BlackRook:
            return self.rook_moves(coord)
        if piece == Pieces.WhiteKnight or piece == Pieces.BlackKnight:
            return self.knight_move(coord)
        if piece == Pieces.WhiteKingBishop or piece == Pieces.WhiteQueenBishop \
            or piece == Pieces.BlackKingBishop or piece == Pieces.BlackQueenBishop:
                return self.bishop_move(coord)
        if piece == Pieces.WhiteQueen or piece == Pieces.BlackQueen:
            return self.queen_move(coord)
        if piece == Pieces.WhiteKing or piece == Pieces.BlackKing:
            return self.king_move(coord)
    
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
    
    # Returns all possible coordinates a knight at the given coordinate could go
    def knight_move(self, coord):
        x,y = coord
        color = Pieces.color( self.grid[y,x] )
        coords = set()
        
        first_move = [-2,2]
        second_move = [-1,1]
        
        # first_move is the two space move, second_move is the 1 space move perpendicular
        for d1 in first_move:
            for d2 in second_move:
                
                # Check moving 2 spaces in x then 1 in y
                if self.in_bounds(x+d1, y+d2) and Pieces.color( self.grid[y+d2, x+d1] ) != color:
                    coords.add( (x+d1, y+d2) )
                # Check moving 2 spaces in y then 1 in x
                if self.in_bounds(x+d2, y+d1) and Pieces.color( self.grid[y+d1, x+d2] ) != color:
                    coords.add( (x+d2, y+d1) )
        
        return coords
    
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
    
    # Returns all possible coordinates a king at the given position could go
    def king_move(self, coord):
        x,y = coord
        color = Pieces.color( self.grid[y,x] )
        coords = set()
        
        # King can move anywhere +/- 1 in x and y
        for i in range(3):
            for j in range(3):
                # x can go to x-1, x, x+1 and y can go to y-1, y, y+1
                # This condition also prevents staying in place
                if self.in_bounds(x+(i-1), y+(j-1)) and color != Pieces.color( self.grid[ y+(j-1), x+(i-1) ] ):
                    coords.add( ( x+(i-1), y+(j-1) ) )
        
        return coords
    
    # Returns all possible coordinates a queen at the given coordinate could go
    # Just the union of all rook and bishop moves
    def queen_move(self, coord):
        return ( self.rook_moves(coord) | self.bishop_move(coord) )
    
    # Returns all the possible coordinates a pawn at the given coordinates can go
    # This allows for two moves if it hasn't yet moved
    def pawn_move(self, coord):
        x,y = coord
        color = Pieces.color( self.grid[y,x] )
        coords = set()
        
        dy = color.value            # Black moves up (-y), white moves down (+y)
        
        if self.grid[y+dy,x] == Pieces.Blank and self.in_bounds(x, y+dy):
            coords.add( (x,y+dy) )
        if ( ( color == Pieces.White and y == 1 ) or (color == Pieces.Black and y == 6 ) ) \
            and ( self.grid[y+(2*dy),x] == Pieces.Blank and self.in_bounds(x, y+(2*dy)) ) :
            # If the pawn hasn't moved yet, it can move two spaces if that space is open
            coords.add( (x, y+(2*dy) ) )
            
        # Pawns can only attack diagonally
        if self.in_bounds(x+1, y+dy) and Pieces.color( self.grid[y+dy, x+1] ) == Pieces.enemy_color(color):
            coords.add( (x+1, y+dy) )
        if self.in_bounds(x-1, y+dy) and Pieces.color( self.grid[y+dy, x-1] ) == Pieces.enemy_color(color):
            coords.add( (x-1, y+dy) )
        
        # TODO : Implement code to swap pawn with captured piece if it makes it to the end
        
        return coords
    
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
    
    # Clone the chess board and return the new instance
    def copy(self):
        clone = Chess()
        clone.grid = np.array( self.grid )
        return clone
    
    # String representation of the chess board
    def __str__(self):
        return ",".join( [ el.value for el in self.grid.flatten() ] )
    
    def printable_grid(self):
        return np.array( (self.__str__()).split(",") ).reshape( (Chess.dimension, Chess.dimension) )