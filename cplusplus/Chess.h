#ifndef CHESS_H_
#define CHESS_H_

#include <vector>
#include <tuple>
#include <set>
#include <cstring>

#include "Pieces.cpp"
#include "Board.h"

const int DIMENSION = 8;

class Chess
{
     public:
        Chess();
        ~Chess() { delete[] grid; };
        
        // Piece functions
        Pieces color(Pieces piece);
        Pieces enemyColor(Pieces color);
        std::string pieceToSymbol(Pieces piece);
        Board* getBoard() { return grid; };
        
        // Chess functions
        void resetBoard();
        void move( std::tuple<int, int> source, std::tuple<int, int> target, Board* board );
        void replace( Board* board );
        std::vector< Board* > generateValidChildren( Pieces turn, Board* board );
        std::vector< Board* > generateChildren( Pieces turn, Board* board );
        std::vector< Board* > promote( Board* board, std::tuple<int,int> coord );
        std::set< std::tuple<int,int> > generateTransitions( Pieces turn, Board* board );
        std::set< std::tuple<int,int> > getPieceCoordinates( Pieces side, Board* board );
        std::set< std::tuple<int,int> > getSpecificPieceCoordinates( Pieces side, Pieces piece, Board* board, bool single );
        std::set< std::tuple<int,int> > getPossibleMoves( std::tuple<int,int> coord, Pieces color, Board* board );
        
        // Functions for the moves of the different pieces
        std::set< std::tuple<int,int> >* rookMoves( std::tuple<int,int> coord, Board* board );
        std::set< std::tuple<int,int> >* knightMoves( std::tuple<int,int> coord, Board* board );
        std::set< std::tuple<int,int> >* bishopMoves( std::tuple<int,int> coord, Board* board );
        std::set< std::tuple<int,int> >* kingMoves( std::tuple<int,int> coord, Board* board );
        std::set< std::tuple<int,int> >* queenMoves( std::tuple<int,int> coord, Board* board );
        std::set< std::tuple<int,int> >* pawnMoves( std::tuple<int,int> coord, Board* board );
        
        // Auxiliary functions
        bool check( Pieces turn, Board* board );
        bool checkMate( Pieces turn, Board* board );
        bool inBounds( int x, int y );
        std::set< std::tuple<int,int> >* crawlDirection( int x, int y, int dx, int dy, std::set< std::tuple<int,int> >* coords, Pieces mover_color, Board* board );
        
        // Developer functions
        int countPieces( Board* board );
        void printGrid( Board* board );
        
    
    private:
        Board* grid;
};

#endif // !CHESS_H_