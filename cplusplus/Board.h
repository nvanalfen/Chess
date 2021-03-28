#ifndef BOARD_H_
#define BOARD_H_

#include "Pieces.cpp"
#include <iostream>

class Board
{
    public:
        Board( int dimension );
        Board( int dimension, Board* clone );
        ~Board();
        
        Pieces index(int x, int y);
        void insert(Pieces element, int x, int y);
        const int getDim() { return dim; };
    
    private:
        int dim;
        Pieces* grid;
};

#endif //!BOARD_H_