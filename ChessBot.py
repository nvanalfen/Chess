# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 18:21:46 2020

@author: nvana
"""

import numpy as np
import pandas as pd
import random
from Chess import Pieces, Chess
import os

# TODO : Implement the following functions
# select_move
# play_move
# train
#
#
#

class ChessBot:
    def __init__(self, side=Pieces.White, learning_file_read_path=None, learning_file_save_path=None,
                 win_score=100, propagation_reduction=1.1, divide_propagate=True):
        self.read_path = None
        self.save_path = None
        self.weights = {}
        self.score = win_score                                          # The score to give a winning grid for learning
        self.propagation = propagation_reduction                        # Value to reduce score by on each step backwards during scoring while learning
        self.divide = divide_propagate                                  # Divide the score by self.propagation each step back. If False, subtract 
        self.board = Chess()                                            # The chess board to play on
        self.check = Pieces.Neutral                                     # The status of whether or not one of the sides is in check. Options are Neutral (no check), White, and Black
        self.checkmate = Pieces.Neutral                                 # Same as check, but with checkmate
        self.side = side                                                # Which side the bot is playing for
        
        self.debug_configs = []
        
        self.set_read_file_path( learning_file_read_path )
        if learning_file_save_path is None:
            self.set_save_file_path( learning_file_read_path )
        else:
            self.set_save_file_path( learning_file_save_path )
        
        self.read_learning_file()
    
    # Set the path to the file containing the probabilities
    def set_read_file_path(self, file_name):
        self.read_path = file_name
    
    # Set the path to the file to save the probabilities
    def set_save_file_path(self, file_name):
        self.save_path = file_name
    
    # Read in the weights
    def read_learning_file(self):
        if not self.read_path is None:
            
            # If the file doesn't exist, make it
            if not os.path.exists( self.read_path ):
                hold = self.save_path
                self.save_path = self.read_path
                self.write_learning_file()
                self.save_path = hold
            
            table = pd.read_csv( self.read_path, index_col=0 )
            
            for ind in table.index:
                self.weights[ ind ] = table["weight"][ind]
    
    # Write the weights to a file for use later
    def write_learning_file(self):
        df = pd.DataFrame.from_dict(self.weights, orient="index", columns=["weight"])
        df.to_csv( self.save_path )
    
    def get_score(self, configuration):
        if not configuration in self.weights:
            return 0
        return self.weights[ configuration ]
    
    # After finishing a game, if one of the sides won, 
    def score_results(self, board_configurations, winner):
        if winner == Pieces.Neutral:
            # If it was a tie, no reason to waste time propagating no score
            return
        
        max_ind = len(board_configurations)-1
        score = (self.score)*winner.value               # White win gets positive score, Black gets negative
        i = 0
        
        for i in range(len(board_configurations)):
            if not board_configurations[ max_ind-i ] in self.weights:
                self.weights[ board_configurations[ max_ind-i ] ] = 0
            
            self.weights[ board_configurations[ max_ind-i ] ] += score
            
            i += 1                                      # Move backwards towards the front of the list
            
            # Lower the score as you get farther away from the winning board
            if self.divide:
                score /= self.propagation
            else:
                score -= self.propagation
    
    # Randomly choose a next move based on the current grid
    def random_choice(self, grid):
        children = self.board.generate_valid_children( self.side, grid )
        if len(children) == 0:
            print( self.board.to_string(grid) )
        return children[ random.choice( np.arange( len(children) ) ) ]
    
    # Find the child with the highest score and return that
    def greedy_choice(self, grid):
        children = self.board.generate_valid_children( self.side, grid )
        best_grid = None
        best_score = 0
        
        for child in children:
            score = self.get_score( self.board.to_string(child) )
            
            # White wants to maximize score, Black wants to minimize
            # By multiplying the score by the value of the side, we can always look for the max
            if self.side.value * score > best_score:
                best_grid = child
                best_score = score
        
        if best_grid is None:
            best_grid = self.random_choice( grid )
        
        return best_grid
    
    # Chooses just by looking at the next level
    # Each child gets minimum of one chance plus one for each point in its score rounded up
    def greedy_pobabilistic_choice(self, grid):
        children = self.board.generate_valid_children( self.side, grid )
        probs = [ 1 for i in range(len(children)) ]
        for i in range(len(children)):
            probs[i] += np.ceil( self.get_score( self.board.to_string( children[i] ) ) )
        if len(children) == 0:
            print( self.board.to_string(grid) )
        return random.choices( children, probs )[0]
    
    # Traverses down several layers of moves and finds the one with the highest score at that layer
    def score_choice(self, grid, max_layers, use_highest):
        children = self.board.generate_valid_children( self.side, grid )
        best = None
        highest = 0
        
        for child in children:
            # Use 2 as layers since this iteration over children is the first layer itself
            score = self.traverse_layers( child, 2, max_layers, self.side, self.side, use_highest=use_highest)
            
            # The child with the best score becomes the current best
            if score > highest:
                highest = score
                best = child
        
        # If no child was chosen, that means that absolutely none of the future generations
        # have scores yet. So just randomly choose
        if best is None:
            best = self.random_choice( grid )
        
        return best
    
    # Traverse to deeper layers to get scores of future generations of boards
    # Parameters:
    #   grid                    ->  numpy array representing the chess board
    #   layer                   ->  The current depth into the traversal
    #   max_layers              ->  The deepest level to traverse to
    #   start_side              ->  The side we're ultimately looking for. Multiply by the
    #                               score so we're always maximizing
    #   side                    ->  The side making the move. Switches on each recursive call
    #   use_highest             ->  Return the highest score found between the start and deepest layer
    #                               If False, sum all the scores from the deepest layer up
    # Returns:
    #   score                   ->  The score found with the parameters given. Used to decide which traversal was best
    def traverse_layers(self, grid, layer, max_layers, start_side, side, use_highest=True):
        children = self.board.generate_valid_children( side, grid )
        score = start_side * self.get_score( self.board.to_string( grid ) )     # Use current score as the base
        
        # Iterate through the children to get the scores
        for child in children:
            temp_score = 0
            
            if layer == max_layers:
                temp_score = start_side * self.get_score( self.board.to_string( child ) )
            else:
                temp_score = self.traverse_layers( child, layer+1, max_layers, start_side, Pieces.enemy_color(side), use_highest )
            
            if not use_highest:
                # Add up the scores returning from the deepest layer
                score += temp_score
            elif temp_score > score:
                # Only keep track of the highest score from the deepest layer
                score = temp_score
        
        return score
    
    # Select the next move to play
    # Parameters:
    #   grid                    ->  numpy array representing the chess board to make a move on
    #   choices                 ->  How to choose the next move
    #                               Options are: random, greedy, greedy probabilistic, max score, sum score
    #   layers                  ->  Number of layers to traverse in the "max score" and "sum score" options
    #   randomize               ->  Allows the algorithm a chance to make a random move, regardless of which move choice is given
    #                               Mostly used for training. Any value below 0 makes it impossible. Between 0 and 1 give some chance
    # Returns:
    #   child                   ->  numpy array representing the board after moving
    def select_move(self, grid, choice="random", layers=5, randomize=-1):
        if choice != "random" and choice != "greedy" and choice != "max score" \
            and choice != "sum score" and choice != "greedy prob":
            print("Unrecognized parameter for choice: ",choice)
        
        if choice == "random" or random.random() < randomize:
            return self.random_choice( grid )
        elif choice == "greedy":
            return self.greedy_choice( grid )
        elif choice == "greedy prob":
            return self.greedy_pobabilistic_choice( grid )
        elif choice == "max score":
            return self.score_choice( grid, layers, True )
        elif choice == "sum score":
            return self.score_choice( grid, layers, False )
        
        # TODO : Implement other choice options?
    
    def move(self, board, choice="random", layers=5, randomize=-1):
        board.replace( self.select_move( board.grid, choice, layers, randomize=randomize) )
    
    # Train the bot
    # Parameters:
    #   choice                      ->  Type of choice selection to use when making moves
    #   layers                      ->  Number of layers to search if using "score" or "sum score" choice selection
    #   training_loops              ->  Number of games to play for training
    #   save_every                  ->  Save weights at intervals of this many rounds
    #   randomize                   ->  Regardless of choice selection type, this number will give a probability
    #                                   of randomly selecting a move to avoid taking the same path every time
    #                                   Setting this number below 0 gives no chance, between 0 and 1 will give that probablitity
    # Returns:
    #   None. The weights are stored and saved
    def train(self, choice="greedy prob", layers=5, training_loops=100, save_every=5, randomize=-1):
        
        white_wins = 0
        black_wins = 0
        ties = 0
        
        for i in range(training_loops):
            print(i)
            self.debug_configs = []
            
            board = Chess()
            configurations = []
            self.side = Pieces.Black
            prev_count = 32
            current_count = 32
            captureless = 0
            winner = Pieces.Neutral
            
            while True:
                if self.side == Pieces.White:
                    self.side = Pieces.Black
                else:
                    self.side = Pieces.White
                
                prev_count = current_count
                
                self.move( board, choice=choice, randomize=randomize )
                configurations.append( str(board) )
                self.debug_configs.append( str(board) )
                
                if board.checkmate( Pieces.enemy_color( self.side ) ):
                    winner = self.side
                    break
                
                current_count = board.count_pieces()
                if current_count == prev_count:
                    captureless += 1
                else:
                    captureless = 0
                if captureless == 50:
                    break
            
            if winner == Pieces.White:
                white_wins +=1
            elif winner == Pieces.Black:
                black_wins += 1
            else:
                ties += 1
            
            print(winner)
            print(white_wins," - ",ties," - ",black_wins,"\n")
            self.score_results( configurations, winner )
            
            if i%save_every == 0:
                self.write_learning_file()
    
    