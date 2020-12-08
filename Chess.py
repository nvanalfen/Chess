# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 18:01:49 2020

@author: nvana
"""
from enum import Enum
import numpy as np

# This refactor (using numpy arrays instead of creating new Chess objects) is 23.5% faster

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
    def move(self, source, target, grid=None):
        if grid is None:
            grid = self.grid
        
        x1, y1 = source
        x2, y2 = target
        
        grid[y2,x2] = grid[y1,x1]                       # Move the piece to the new location
        grid[y1,x1] = Pieces.Blank                      # Replace the old location with a blank
        
        return grid
    
    def replace(self, grid):
        self.grid = grid
    
    def generate_valid_children(self, turn, grid=None):
        if grid is None:
            grid = self.grid
            
        children = []
        for child in self.generate_children(turn, grid):
            if not self.check(child, turn):
                children.append( child )
        return children
    
    # Generates all possible grids that can be reached in one move from the current grid
    # Parameters:
    #   turn        ->  Pieces.Black or Pieces.White, whoever's turn it is to move
    #   grid        ->  numpy array representing the chess board
    # Returns:
    #   children    ->  list of numpy arrays representing the grid configuration
    def generate_children(self, turn, grid=None):
        if grid is None:
            grid = self.grid
            
        transitions = self.generate_transitions(turn, grid)
        children = []
        for source, target in transitions:
            child = np.array( grid )                    # Copy the current grid
            child = self.move(source, target, child)    # Make the move
            
            if ( child[target[1],target[0]] == Pieces.WhitePawn and target[1] == Chess.dimension-1 ) \
                or ( child[target[1],target[0]] == Pieces.BlackPawn and target[1] == 0 ):
                children += self.promote(child, target)
            else:
                children.append( child )
        
        return children
    
    # Generates all start to end transitions that can be made from the current grid
    # Parameters:
    #   turn        ->  Pieces.Black or Pieces.White, whoever's turn it is to move
    # Returns:
    #   transitions ->  list of 2-tuples where each element is a 2-tuple representing an (x,y) coordinate
    #                   the first 2-tuple is the start point, the second is the end point
    def generate_transitions(self, turn, grid=None):
        if grid is None:
            grid = self.grid
            
        sources = self.get_piece_coordinates(turn, grid)
        
        transitions = []
        for source in sources:
            targets = self.get_possible_moves(source, turn, grid)
            for target in targets:
                transitions.append( (source, target) )
        
        return transitions
    
    # Get the coordinates for all the existing pieces of one player
    # Parameters:
    #   side                ->  Color of one of the players. Pieces.White or Pieces.Black
    # Returns:
    #   coords              ->  set of (x,y) coordinate tuples for the coordinates of each piece
    def get_piece_coordinates(self, side, grid=None):
        if grid is None:
            grid = self.grid
        coords = set()
        
        for y in range(Chess.dimension):
            for x in range(Chess.dimension):
                if Pieces.color( grid[y,x] ) == side:
                    coords.add( (x,y) )
        return coords
    
    def get_all_possible_moves(self, turn):
        pass
    
    # Given a coordinate, decide which type of piece it is and return moves appropriate for that
    # Parameters:
    #   coord       ->  2-tuple of (x,y) coordinate where the piece in question is located
    # Returns:
    #   coords      ->  set of 2-tuples of (x,y) coordinates where the piece in question could move
    def get_possible_moves(self, coord, color, grid=None):
        if grid is None:
            grid = self.grid
            
        x,y = coord
        piece = grid[y,x]
        
        if piece == Pieces.WhitePawn or piece == Pieces.BlackPawn:
            return self.pawn_move(coord, grid)
        if piece == Pieces.WhiteRook or piece == Pieces.BlackRook:
            return self.rook_moves(coord, grid)
        if piece == Pieces.WhiteKnight or piece == Pieces.BlackKnight:
            return self.knight_move(coord, grid)
        if piece == Pieces.WhiteKingBishop or piece == Pieces.WhiteQueenBishop \
            or piece == Pieces.BlackKingBishop or piece == Pieces.BlackQueenBishop:
                return self.bishop_move(coord, grid)
        if piece == Pieces.WhiteQueen or piece == Pieces.BlackQueen:
            return self.queen_move(coord, grid)
        if piece == Pieces.WhiteKing or piece == Pieces.BlackKing:
            return self.king_move(coord, grid)
    
    # TODO : Remove any moves that place your own side in check
    
    # Returns all possible coordinates a rook at the given coordinate could go
    def rook_moves(self, coord, grid=None):
        if grid is None:
            grid = self.grid
            
        x,y = coord
        color = Pieces.color( self.grid[y,x] )
        coords = set()
        self.crawl_direction(x+1, y, 1, 0, coords, color, grid)
        self.crawl_direction(x-1, y, -1, 0, coords, color, grid)
        self.crawl_direction(x, y+1, 0, 1, coords, color, grid)
        self.crawl_direction(x, y-1, 0, -1, coords, color, grid)
        
        return coords
    
    # Returns all possible coordinates a knight at the given coordinate could go
    def knight_move(self, coord, grid=None):
        if grid is None:
            grid = self.grid
            
        x,y = coord
        color = Pieces.color( grid[y,x] )
        coords = set()
        
        first_move = [-2,2]
        second_move = [-1,1]
        
        # first_move is the two space move, second_move is the 1 space move perpendicular
        for d1 in first_move:
            for d2 in second_move:
                
                # Check moving 2 spaces in x then 1 in y
                if self.in_bounds(x+d1, y+d2) and Pieces.color( grid[y+d2, x+d1] ) != color:
                    coords.add( (x+d1, y+d2) )
                # Check moving 2 spaces in y then 1 in x
                if self.in_bounds(x+d2, y+d1) and Pieces.color( grid[y+d1, x+d2] ) != color:
                    coords.add( (x+d2, y+d1) )
        
        return coords
    
    # Returns all possible coordinates a bishop at the given coordinate could go
    def bishop_move(self, coord, grid=None):
        if grid is None:
            grid = self.grid
            
        x,y = coord
        color = Pieces.color( grid[y,x] )
        coords = set()
        self.crawl_direction(x+1, y+1, 1, 1, coords, color, grid)
        self.crawl_direction(x+1, y-1, 1, -1, coords, color, grid)
        self.crawl_direction(x-1, y+1, -1, 1, coords, color, grid)
        self.crawl_direction(x-1, y-1, -1, -1, coords, color, grid)
        
        return coords
    
    # Returns all possible coordinates a king at the given position could go
    def king_move(self, coord, grid=None):
        if grid is None:
            grid = self.grid
            
        x,y = coord
        color = Pieces.color( grid[y,x] )
        coords = set()
        
        # King can move anywhere +/- 1 in x and y
        for i in range(3):
            for j in range(3):
                # x can go to x-1, x, x+1 and y can go to y-1, y, y+1
                # This condition also prevents staying in place
                if self.in_bounds(x+(i-1), y+(j-1)) and color != Pieces.color( grid[ y+(j-1), x+(i-1) ] ):
                    coords.add( ( x+(i-1), y+(j-1) ) )
        
        return coords
    
    # Returns all possible coordinates a queen at the given coordinate could go
    # Just the union of all rook and bishop moves
    def queen_move(self, coord, grid):
        if grid is None:
            grid = self.grid
        return ( self.rook_moves(coord, grid) | self.bishop_move(coord, grid) )
    
    # Returns all the possible coordinates a pawn at the given coordinates can go
    # This allows for two moves if it hasn't yet moved
    def pawn_move(self, coord, grid=None):
        if grid is None:
            grid = self.grid
            
        x,y = coord
        color = Pieces.color( grid[y,x] )
        coords = set()
        
        dy = color.value            # Black moves up (-y), white moves down (+y)
        
        if self.in_bounds(x, y+dy) and grid[y+dy,x] == Pieces.Blank:
            coords.add( (x,y+dy) )
        if ( ( color == Pieces.White and y == 1 ) or (color == Pieces.Black and y == 6 ) ) \
            and ( grid[y+(2*dy),x] == Pieces.Blank and self.in_bounds(x, y+(2*dy)) ) :
            # If the pawn hasn't moved yet, it can move two spaces if that space is open
            coords.add( (x, y+(2*dy) ) )
            
        # Pawns can only attack diagonally
        if self.in_bounds(x+1, y+dy) and Pieces.color( grid[y+dy, x+1] ) == Pieces.enemy_color(color):
            coords.add( (x+1, y+dy) )
        if self.in_bounds(x-1, y+dy) and Pieces.color( grid[y+dy, x-1] ) == Pieces.enemy_color(color):
            coords.add( (x-1, y+dy) )
        
        # TODO : Implement code to swap pawn with captured piece if it makes it to the end
        
        return coords
    
    # Promotes a pawn to another piece if it makes it to the other side of the board
    # Takes a child grid and returns all possible copies of the grid with different promotions
    # Parameters:
    #   child           ->  numpy array to clone and replace with promotions
    #   coord           ->  (x,y) tuple of grid location for the pawn to be promoted
    # Returns:
    #   children        ->  list of children of current chess object, numpy arrays
    def promote(self, child, coord):
            
        x,y = coord
        color = Pieces.color( child[y,x] )
        
        promotions = []
        children = []
        if color == Pieces.White:
            promotions = [Pieces.WhiteRook, Pieces.WhiteKnight, Pieces.WhiteQueen, \
                          Pieces.WhiteKingBishop, Pieces.WhiteQueenBishop]
        elif color == Pieces.Black:
            promotions = [Pieces.BlackRook, Pieces.BlackKnight, Pieces.BlackQueen, \
                          Pieces.BlackKingBishop, Pieces.BlackQueenBishop]
        
        for piece in promotions:
            clone = np.array( child )
            clone[y,x] = piece
            children.append( clone )
        
        return children
    
    # Checks to see if the current position puts a certain side in check
    # Check is true if any of the children grids are missing the king
    # Parameters:
    #   board               ->  The chess board layout to check. numpy array
    #   turn                ->  The color to see if its in check. Pieces.Black or Pieces.White
    # Returns:
    #   check               ->  True if the player with the color of the turn variable is in check
    def check(self, board, turn):
        
        # Determing which king is the 
        king = None
        if turn == Pieces.White:
            king = Pieces.WhiteKing
        else:
            king = Pieces.BlackKing
        
        # Check all of the children to see if any of them are missing the king
        for child in self.generate_children( Pieces.enemy_color(turn), board ):
            if not king in child.flatten():
                return True
        
        return False
    
    # Checks to see if the current grid is in checkmate for the player of the given color
    # Checkmate for turn if all moves from the turn side results in check for turn
    # Parameters:
    #   turn                ->  Pieces.White or Pieces.Black. The color of the player we're checking to see if is in checkmate
    # Returns:
    #   cm                  ->  True if the turn color is in checkmate
    def checkmate(self, turn, grid=None):
        if grid is None:
            grid = self.grid
            
        for child in self.generate_children(turn, grid):
            if not self.check( child, turn ):
                return False
        return True
    
    # Checks to see if a coordinate is still on the grid
    def in_bounds(self, x, y):
        return x >= 0 and x < Chess.dimension and y >= 0 and y < Chess.dimension
    
    # Continues crawling in a given direction until a collision
    # Returns a set of all possible coordinates encountered
    def crawl_direction(self, x, y, dx, dy, coords, mover_color, grid=None):
        if grid is None:
            grid = self.grid
        
        # If we have left the grid or would hit one of our own pieces, it's not a valid move
        if not self.in_bounds(x,y) or mover_color == Pieces.color( grid[y,x] ):
            return
        
        coords.add( (x,y) )
        
        # If we haven't taken another piece, we can still move
        if grid[y,x] == Pieces.Blank:
            self.crawl_direction(x+dx, y+dy, dx, dy, coords, mover_color, grid)
    
    def count_pieces(self, grid=None):
        if grid is None:
            grid = self.grid
        return (Chess.dimension * Chess.dimension) - sum( [ el == Pieces.Blank for el in grid.flatten() ] )
    
    # Clone the chess board and return the new instance
    def copy(self):
        clone = Chess()
        clone.grid = np.array( self.grid )
        return clone
    
    # Clone just the numpy array, not the whole object
    def copy_grid(self, grid):
        return np.array(grid)
    
    def to_string(self, grid):
        return ",".join( [ el.value for el in grid.flatten() ] )
    
    # String representation of the chess board
    def __str__(self):
        return ",".join( [ el.value for el in self.grid.flatten() ] )
    
    def printable_grid(self):
        return np.array( (self.__str__()).split(",") ).reshape( (Chess.dimension, Chess.dimension) )