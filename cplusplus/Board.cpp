#include "Board.h"
#include <iostream>

Board::Board( int dimension )
{
    dim = dimension;
    grid = new Pieces[ dim*dim ];
    for(int i = 0; i < dimension; i++)
    {
        for(int j = 0; j < dim; j++)
        {
            insert( Pieces::NEUTRAL, i, j );
        }
    }
}

Board::Board( int dimension, Board* clone )
{
    dim = dimension;
    grid = new Pieces[ dim*dim ];
    for(int i = 0; i < dimension; i++)
    {
        for(int j = 0; j < dim; j++)
        {
            insert( clone->index(i,j), i, j );
        }
    }
}

Board::~Board()
{
    delete[] grid;
}

Pieces Board::index( int x, int y )
{
    return grid[ y*dim + x ];
}

void Board::insert( Pieces element, int x, int y )
{
    grid[ y*dim + x ] = element;
}