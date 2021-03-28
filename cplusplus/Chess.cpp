#include "Chess.h"
#include <iostream>

// Tested Functions (+ means has been tested, - means not yet tested):
// + color
// + enemyColor
// + pieceToSymbol
// + resetBoard
// + move
// + replace
// - generateValidChildren
// - generateChildren
// - promote
// - generateTransitions
// - setPieceCoordinates
// - setSpecificCoordinates
// - getPossibleMoves
// + rookMoves
// + knightMoves
// + bishopMoves
// - kingMoves
// - queenMoves
// - pawnMoves
// - check
// - checkMate
// + inBounds
// + crawlDirection
// + countPieces
// + printGrid

Chess::Chess()
{
    grid = NULL;
    resetBoard();
}

// Piece functions

// Returns the color of a given piece
Pieces Chess::color(Pieces piece)
{
    if( int(piece) > 0 )
    {
        return Pieces::WHITE;
    }
    else if( int(piece) < 0 )
    {
        return Pieces::BLACK;
    }
    return Pieces::NEUTRAL;
}

// Returns the enemy color of the one given
Pieces Chess::enemyColor(Pieces color)
{
    if( color == Pieces::WHITE )
    {
        return Pieces::BLACK;
    }
    else if( color == Pieces::BLACK )
    {
        return Pieces::WHITE;
    }
    return Pieces::NEUTRAL;
}

// Return the symbol associated with the piece
// Mostly for display and debugging
 std::string Chess::pieceToSymbol(Pieces piece)
{
    if( piece == Pieces::NEUTRAL )
    {
        return "X";
    }
    
     std::string symbol = "";
    
    if( color(piece) == Pieces::WHITE )
    {
        symbol += "W";
    }
    else if( color(piece) == Pieces::BLACK )
    {
        symbol += "B";
    }
    
    if( piece == Pieces::WHITEPAWN || piece == Pieces::BLACKPAWN )
    {
        symbol += "P";
    }
    else if( piece == Pieces::WHITEROOK || piece == Pieces::BLACKROOK )
    {
        symbol += "R";
    }
    else if( piece == Pieces::WHITEKNIGHT || piece == Pieces::BLACKKNIGHT )
    {
        symbol += "kn";
    }
    else if( piece == Pieces::WHITEKINGBISHOP || piece == Pieces::WHITEQUEENBISHOP
                || piece == Pieces::BLACKKINGBISHOP || piece == Pieces::BLACKQUEENBISHOP)
    {
        symbol += "B";
    }
    else if( piece == Pieces::WHITEKING || piece == Pieces::BLACKKING )
    {
        symbol += "K";
    }
    else if( piece == Pieces::WHITEQUEEN || piece == Pieces::BLACKQUEEN )
    {
        symbol += "Q";
    }
    
    return symbol;
}

// Chess functions

// Resets the board to the new starting position
void Chess::resetBoard()
{
    delete[] grid;
    grid = new Board(DIMENSION);
    
    // Set up white pieces
    grid->insert(Pieces::WHITEROOK, 0, 0);
    grid->insert(Pieces::WHITEROOK, 7, 0);
    grid->insert(Pieces::WHITEKNIGHT, 1, 0);
    grid->insert(Pieces::WHITEKNIGHT, 6, 0);
    grid->insert(Pieces::WHITEKINGBISHOP, 2, 0);
    grid->insert(Pieces::WHITEKING, 3, 0);
    grid->insert(Pieces::WHITEQUEEN, 4, 0);
    grid->insert(Pieces::WHITEQUEENBISHOP, 5, 0);
    for(int i = 0; i < DIMENSION; i++)
    {
        grid->insert(Pieces::WHITEPAWN, i, 1);
    }
    
    // Set up black pieces
    grid->insert(Pieces::BLACKROOK, 0, DIMENSION-1);
    grid->insert(Pieces::BLACKROOK, 7, DIMENSION-1);
    grid->insert(Pieces::BLACKKNIGHT, 1, DIMENSION-1);
    grid->insert(Pieces::BLACKKNIGHT, 6, DIMENSION-1);
    grid->insert(Pieces::BLACKKINGBISHOP, 2, DIMENSION-1);
    grid->insert(Pieces::BLACKKING, 3, DIMENSION-1);
    grid->insert(Pieces::BLACKQUEEN, 4, DIMENSION-1);
    grid->insert(Pieces::BLACKQUEENBISHOP, 5, DIMENSION-1);
    for(int i = 0; i < DIMENSION; i++)
    {
        grid->insert(Pieces::BLACKPAWN, i, DIMENSION-2);
    }
}

// Move a piece from source coordinates to target coordinates
void Chess::move( std::tuple<int, int> source, std::tuple<int, int> target, Board* board )
{
    if( board == NULL )
    {
        board = grid;
    }
    
    int source_x = std::get<0>(source);
    int source_y = std::get<1>(source);
    int target_x = std::get<0>(target);
    int target_y = std::get<1>(target);
    
    if( !inBounds( source_x, source_y ) || !inBounds( target_x, target_y ) )
    {
        return;                     // Avoid attempting to access out of bounds indices
    }
    
    grid->insert( grid->index(source_x, source_y), target_x, target_y );        // Move the source to the target
    grid->insert( Pieces::NEUTRAL, source_x, source_y );                             // Replace the source with a blank space
}

// Replace the grid with a new one
void Chess::replace( Board* board )
{
    for(int i = 0; i < DIMENSION; i++)
    {
        for(int j = 0; j < DIMENSION; j++)
        {
            grid->insert( board->index( i, j ), i, j );
        }
    }
}

std::vector< Board* > Chess::generateValidChildren( Pieces turn, Board* board )
{
    return std::vector< Board* >();
}

std::vector< Board* > Chess::generateChildren( Pieces turn, Board* board )
{
    return std::vector< Board* >();
}

std::vector< Board* > Chess::promote( Board* board, std::tuple<int,int> coord )
{
    return std::vector< Board* >();
}

std::set< std::tuple<int,int> > Chess::generateTransitions( Pieces turn, Board* board )
{
    return std::set< std::tuple<int,int> >();
}

std::set< std::tuple<int,int> > Chess::getPieceCoordinates( Pieces side, Board* board )
{
    return std::set< std::tuple<int,int> >();
}

std::set< std::tuple<int,int> > Chess::getSpecificPieceCoordinates( Pieces side, Pieces piece, Board* board, bool single )
{
    return std::set< std::tuple<int,int> >();
}

std::set< std::tuple<int,int> > Chess::getPossibleMoves( std::tuple<int,int> coord, Pieces color, Board* board )
{
    return std::set< std::tuple<int,int> >();
}

bool Chess::check( Pieces turn, Board* board )
{
    return false;
}

std::set< std::tuple<int,int> >* Chess::rookMoves( std::tuple<int,int> coord, Board* board )
{
    if( board == NULL )
    {
        board = grid;
    }
    
    std::set< std::tuple<int,int> >* coords = new std::set< std::tuple<int,int> >();
    
    int source_x = std::get<0>(coord);
    int source_y = std::get<1>(coord);
    Pieces piece_color = color( grid->index(source_x, source_y) );
    
    coords = crawlDirection(source_x+1, source_y, 1, 0, coords, piece_color, board);
    coords = crawlDirection(source_x-1, source_y, -1, 0, coords, piece_color, board);
    coords = crawlDirection(source_x, source_y+1, 0, 1, coords, piece_color, board);
    coords = crawlDirection(source_x, source_y-1, 0, -1, coords, piece_color, board);
    
    return coords;
}

std::set< std::tuple<int,int> >* Chess::knightMoves( std::tuple<int,int> coord, Board* board )
{
    if( board == NULL )
    {
        board = grid;
    }
    
    std::set< std::tuple<int,int> >* coords = new std::set< std::tuple<int,int> >();
    
    int x = std::get<0>(coord);
    int y = std::get<1>(coord);
    Pieces piece_color = color( grid->index(x, y) );
    
    // First move is a 2 space move in any direction
    // Second move is a 1 space move in a perpendicular direction
    for( auto d1 : {-2,2} )
    {
        for( auto d2 : {-1,1} )
        {
            
            // Check moving 2 spaces in x then 1 in y
            if( inBounds(x+d1, y+d2) && color( board->index(x+d1, y+d2) ) != piece_color )
            {
                coords->insert( {x+d1, y+d2} );
            }
            // Check meving 2 spaces in y then 1 in x
            if( inBounds(x+d2, y+d1) && color( board->index(x+d2, y+d1) ) != piece_color )
            {
                coords->insert( {x+d2, y+d1} );
            }
            
        }
    }
    
    return coords;
    
}

std::set< std::tuple<int,int> >* Chess::bishopMoves( std::tuple<int,int> coord, Board* board )
{
    if( board == NULL )
    {
        board = grid;
    }
    
    std::set< std::tuple<int,int> >* coords = new std::set< std::tuple<int,int> >();
    
    int source_x = std::get<0>(coord);
    int source_y = std::get<1>(coord);
    Pieces piece_color = color( grid->index(source_x, source_y) );
    
    coords = crawlDirection(source_x+1, source_y+1, 1, 1, coords, piece_color, board);
    coords = crawlDirection(source_x+1, source_y-1, 1, -1, coords, piece_color, board);
    coords = crawlDirection(source_x-1, source_y+1, -1, 1, coords, piece_color, board);
    coords = crawlDirection(source_x-1, source_y-1, -1, -1, coords, piece_color, board);
    
    return coords;
}

std::set< std::tuple<int,int> >* Chess::kingMoves( std::tuple<int,int> coord, Board* board )
{
    
}

std::set< std::tuple<int,int> >* queenMoves( std::tuple<int,int> coord, Board* board );
std::set< std::tuple<int,int> >* pawnMoves( std::tuple<int,int> coord, Board* board );

bool Chess::checkMate( Pieces turn, Board* board )
{
    return false;
}

bool Chess::inBounds( int x, int y )
{
    return ( x >= 0 && x < DIMENSION && y >= 0 && y < DIMENSION );
}

std::set< std::tuple<int,int> >* Chess::crawlDirection( int x, int y, int dx, int dy, std::set< std::tuple<int,int> >* coords, Pieces mover_color, Board* board )
{
    if( board == NULL )
    {
        board = grid;
    }
        
    if( !inBounds(x, y) || mover_color == color( board->index(x,y) ) )
    {
        return coords;
    }
    
    coords->insert( {x, y} );
    
    // If we haven't yet taken a piece, we can still move
    if( board->index(x,y) == Pieces::NEUTRAL )
    {
        coords = crawlDirection( x+dx, y+dy, dx, dy, coords, mover_color, board );
    }
    
    return coords;
}

int Chess::countPieces( Board* board )
{
    if(board == NULL)
    {
        board = grid;
    }
    
    int count = 0;
    for(int i = 0; i < DIMENSION; i++)
    {
        for(int j = 0; j < DIMENSION; j++)
        {
            if( grid->index(i,j) != Pieces::NEUTRAL )
            {
                count++;
            }
        }
    }
    
    return count;
}

void Chess::printGrid( Board* board )
{
    if(board == NULL)
    {
        board = grid;
    }
    
    for(int j = 0; j < DIMENSION; j++)
    {
        for(int i = 0; i < DIMENSION; i++)
        {
            std::cout << pieceToSymbol( board->index(i,j) );
            if( i < DIMENSION-1 )
            {
                std::cout << ",\t";
            }
        }
        std::cout << std::endl;
    }
}