#include <iostream>
#include "Chess.cpp"
#include "Pieces.cpp"
#include "Board.cpp"

int main()
{
    //Pieces temp = Pieces::WHITEROOK;
    Chess game = Chess();
    Board* board = game.getBoard();
    
    std::set< std::tuple<int,int> >* temp = new std::set< std::tuple<int,int> >();
    
    /*
    board->insert(Pieces::WHITEKINGBISHOP,5,5);
    game.printGrid(NULL);
    temp = game.bishopMoves( {5,5}, NULL );
    
    
    for( auto current : *temp)
    {
        std::cout << std::get<0>(current) << "," << std::get<1>(current) << std::endl;
        std::cout << game.pieceToSymbol( board->index(std::get<0>(current), std::get<1>(current)) ) << std::endl;
    }
    */
    
    
    
    return 0;
}