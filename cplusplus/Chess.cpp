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
// + generateChildren (BUGS)
// + promote
// + generateTransitions
// + getPieceCoordinates
// - getSpecificCoordinates
// - getPossibleMoves (WRITTEN BUT UNTESTED)
// + rookMoves
// + knightMoves
// + bishopMoves
// + kingMoves
// + queenMoves
// + pawnMoves
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
    else if( piece == Pieces::WHITEBISHOP || piece == Pieces::BLACKBISHOP)
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
    grid->insert(Pieces::WHITEBISHOP, 2, 0);
    grid->insert(Pieces::WHITEKING, 3, 0);
    grid->insert(Pieces::WHITEQUEEN, 4, 0);
    grid->insert(Pieces::WHITEBISHOP, 5, 0);
    for(int i = 0; i < DIMENSION; i++)
    {
        grid->insert(Pieces::WHITEPAWN, i, 1);
    }
    
    // Set up black pieces
    grid->insert(Pieces::BLACKROOK, 0, DIMENSION-1);
    grid->insert(Pieces::BLACKROOK, 7, DIMENSION-1);
    grid->insert(Pieces::BLACKKNIGHT, 1, DIMENSION-1);
    grid->insert(Pieces::BLACKKNIGHT, 6, DIMENSION-1);
    grid->insert(Pieces::BLACKBISHOP, 2, DIMENSION-1);
    grid->insert(Pieces::BLACKKING, 3, DIMENSION-1);
    grid->insert(Pieces::BLACKQUEEN, 4, DIMENSION-1);
    grid->insert(Pieces::BLACKBISHOP, 5, DIMENSION-1);
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
    
    board->insert( board->index(source_x, source_y), target_x, target_y );        // Move the source to the target
    board->insert( Pieces::NEUTRAL, source_x, source_y );                               // Replace the source with a blank space
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
    if( board == NULL )
    {
        board = grid;
    }
    
    std::vector< Board* > children = std::vector< Board* >();
    for( auto child : generateChildren(turn, board) )
    {
        if( !check( turn, child ) )
        {
            children.push_back( child );
        }
    }
    
    return children;
}

std::vector< Board* > Chess::generateChildren( Pieces turn, Board* board )
{
    if( board == NULL )
    {
        board = grid;
    }
    
    std::set< std::tuple< std::tuple<int,int>, std::tuple<int,int> > > transitions = generateTransitions( turn, board );
    std::vector< Board* > children = std::vector< Board* >();
    
    for( auto pair : transitions )
    {
        std::tuple<int,int> source = std::get<0>(pair);
        std::tuple<int,int> target = std::get<1>(pair);
        
        Board* child = new Board(DIMENSION, board);         // Copy the current grid
        move( source, target, child );                                    // Make the move
        
        int tar_x = std::get<0>(target);
        int tar_y = std::get<1>(target);
        if( ( child->index(tar_x, tar_y) == Pieces::WHITEPAWN && tar_y == DIMENSION-1 ) 
            || ( child->index(tar_x, tar_y) == Pieces::BLACKPAWN && tar_y == 0 ) )
        {
            std::vector< Board* > promotions = promote( child, target );
            children.insert( children.end(), promotions.begin(), promotions.end() );
        }
        else
        {
            children.push_back( child );
        }
        
    }
    
    return children;
}

// Promotes a pawn to another piece if it makes it to the other side of the board
std::vector< Board* > Chess::promote( Board* board, std::tuple<int,int> coord )
{
    if( board == NULL )
    {
        board = grid;
    }
    
    int x = std::get<0>(coord);
    int y = std::get<1>(coord);
    Pieces piece_color = color( board->index(x, y) );
    
    std::set< Pieces > promotions;
    std::vector< Board* > children = std::vector< Board* >();
    if( piece_color == Pieces::WHITE )
    {
        promotions = { Pieces::WHITEROOK, Pieces::WHITEKNIGHT, Pieces::WHITEQUEEN,
                Pieces::WHITEBISHOP };
    }
    else if( piece_color == Pieces::BLACK )
    {
        promotions = { Pieces::BLACKROOK, Pieces::BLACKKNIGHT, Pieces::BLACKQUEEN,
                Pieces::BLACKBISHOP };
    }
    
    for( auto piece : promotions )
    {
        Board* clone = new Board( DIMENSION, board );
        clone->insert( piece, x, y );
        children.push_back(clone);
    }
    
    return children;
}

std::set< std::tuple< std::tuple<int,int>, std::tuple<int,int> > > Chess::generateTransitions( Pieces turn, Board* board )
{
    if( board == NULL )
    {
        board = grid;
    }
    
    std::set< std::tuple<int,int> > sources = getPieceCoordinates( turn, board );
    std::set< std::tuple< std::tuple<int,int>, std::tuple<int,int> > > transitions = std::set< std::tuple< std::tuple<int,int>, std::tuple<int,int> > >();
    
    for( auto source : sources )
    {
        //std::cout << "Source: " << std::get<0>(source) << "," << std::get<1>(source) << std::endl;
        std::set< std::tuple<int,int> > targets = getPossibleMoves( source, turn, board );
        for( auto target : targets )
        {
            transitions.insert( { source, target } );
        }
    }
    
    return transitions;
}

std::set< std::tuple<int,int> > Chess::getPieceCoordinates( Pieces side, Board* board )
{
    if( board == NULL )
    {
        board = grid;
    }
    
    std::set< std::tuple<int,int> > coords = std::set< std::tuple<int,int> >();
    
    for(int j = 0; j < DIMENSION; j++)
    {
        for(int i = 0; i < DIMENSION; i++)
        {
            if( color( board->index(i,j) ) == side )
            {
                coords.insert( {i, j} );
            }
        }
    }
    
    return coords;
}

std::set< std::tuple<int,int> > Chess::getSpecificPieceCoordinates( Pieces side, Pieces piece, Board* board, bool single )
{
    if( board == NULL )
    {
        board = grid;
    }
    
    std::set< std::tuple<int,int> > coords = std::set< std::tuple<int,int> >();
    
    return std::set< std::tuple<int,int> >();
}

std::set< std::tuple<int,int> > Chess::getPossibleMoves( std::tuple<int,int> coord, Pieces color, Board* board )
{
    if( board == NULL )
    {
        board = grid;
    }
    
    int x = std::get<0>(coord);
    int y = std::get<1>(coord);
    Pieces piece = board->index(x,y);
    
    if( piece == Pieces::WHITEPAWN || piece == Pieces::BLACKPAWN )
    {
        return pawnMoves( coord, board );
    }
    if( piece == Pieces::WHITEROOK || piece == Pieces::BLACKROOK )
    {
        return rookMoves( coord, board );
    }
    if( piece == Pieces::WHITEKNIGHT || piece == Pieces::BLACKKNIGHT )
    {
        return knightMoves( coord, board );
    }
    if( piece == Pieces::WHITEBISHOP || piece == Pieces::BLACKBISHOP )
    {
        return bishopMoves( coord, board );
    }
    if( piece == Pieces::WHITEQUEEN || piece == Pieces::BLACKQUEEN )
    {
        return queenMoves( coord, board );
    }
    if( piece == Pieces::WHITEKING || piece == Pieces::BLACKKING)
    {
        return kingMoves( coord, board );
    }
    
    return std::set< std::tuple<int,int> >();
    
}

std::set< std::tuple<int,int> > Chess::rookMoves( std::tuple<int,int> coord, Board* board )
{
    if( board == NULL )
    {
        board = grid;
    }
    
    std::set< std::tuple<int,int> > coords = std::set< std::tuple<int,int> >();
    
    int source_x = std::get<0>(coord);
    int source_y = std::get<1>(coord);
    Pieces piece_color = color( grid->index(source_x, source_y) );
    
    coords = crawlDirection(source_x+1, source_y, 1, 0, coords, piece_color, board);
    coords = crawlDirection(source_x-1, source_y, -1, 0, coords, piece_color, board);
    coords = crawlDirection(source_x, source_y+1, 0, 1, coords, piece_color, board);
    coords = crawlDirection(source_x, source_y-1, 0, -1, coords, piece_color, board);
    
    return coords;
}

std::set< std::tuple<int,int> > Chess::knightMoves( std::tuple<int,int> coord, Board* board )
{
    if( board == NULL )
    {
        board = grid;
    }
    
    std::set< std::tuple<int,int> > coords = std::set< std::tuple<int,int> >();
    
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
                coords.insert( {x+d1, y+d2} );
            }
            // Check meving 2 spaces in y then 1 in x
            if( inBounds(x+d2, y+d1) && color( board->index(x+d2, y+d1) ) != piece_color )
            {
                coords.insert( {x+d2, y+d1} );
            }
            
        }
    }
    
    return coords;
    
}

std::set< std::tuple<int,int> > Chess::bishopMoves( std::tuple<int,int> coord, Board* board )
{
    if( board == NULL )
    {
        board = grid;
    }
    
    std::set< std::tuple<int,int> > coords = std::set< std::tuple<int,int> >();
    
    int source_x = std::get<0>(coord);
    int source_y = std::get<1>(coord);
    Pieces piece_color = color( grid->index(source_x, source_y) );
    
    coords = crawlDirection(source_x+1, source_y+1, 1, 1, coords, piece_color, board);
    coords = crawlDirection(source_x+1, source_y-1, 1, -1, coords, piece_color, board);
    coords = crawlDirection(source_x-1, source_y+1, -1, 1, coords, piece_color, board);
    coords = crawlDirection(source_x-1, source_y-1, -1, -1, coords, piece_color, board);
    
    return coords;
}

std::set< std::tuple<int,int> > Chess::kingMoves( std::tuple<int,int> coord, Board* board )
{
    if( board == NULL )
    {
        board = grid;
    }
    
    std::set< std::tuple<int,int> > coords = std::set< std::tuple<int,int> >();
    
    int x = std::get<0>(coord);
    int y = std::get<1>(coord);
    Pieces piece_color = color( grid->index(x, y) );
    
    // King can move anywhere +/- 1 in x and/or y
    for(int i = 0; i < 3; i++)
    {
        for(int j = 0; j < 3; j++)
        {
            // x can go to x-1, x, x+1 and y can go to y-1, y, y+1
            // This condition also prevents staying in place
            if( inBounds( x+(i-1), y+(j-1) ) && piece_color != color( board->index( x+(i-1), y+(j-1) ) ) )
            {
                coords.insert( { x+(i-1), y+(j-1) } );
            }
        }
    }
    
    return coords;
    
}

std::set< std::tuple<int,int> > Chess::queenMoves( std::tuple<int,int> coord, Board* board )
{
    if( board == NULL )
    {
        board = grid;
    }
    
    std::set< std::tuple<int,int> > coords = std::set< std::tuple<int,int> >();
    
    // The queen's moves are just a combination of the rook's and bishop's
    std::set< std::tuple<int,int> > rook_coords = rookMoves( coord, board );
    std::set< std::tuple<int,int> > bishop_coords = bishopMoves( coord, board );
    
    // Merge the two results
    coords.insert( rook_coords.begin(), rook_coords.end() );
    coords.insert( bishop_coords.begin(), bishop_coords.end() );
    
    return coords;
}

std::set< std::tuple<int,int> > Chess::pawnMoves( std::tuple<int,int> coord, Board* board )
{
    if( board == NULL )
    {
        board = grid;
    }
    
    std::set< std::tuple<int,int> > coords = std::set< std::tuple<int,int> >();
    
    int x = std::get<0>(coord);
    int y = std::get<1>(coord);
    Pieces piece_color = color( grid->index(x, y) );
    
    int dy = int(piece_color);                  // Black moves up (-y), white moves down (+y)
    
    if( inBounds(x, y+dy) && board->index( x, y+dy ) == Pieces::NEUTRAL )
    {
        coords.insert( {x, y+dy} );
    }
    if( ( ( piece_color == Pieces::WHITE && y == 1 ) || ( piece_color == Pieces::BLACK && y == DIMENSION-2 ) ) && 
        inBounds( x, y+(2*dy) ) && ( board->index( x, y+dy ) == Pieces::NEUTRAL ) && ( board->index( x, y+(2*dy) ) == Pieces::NEUTRAL ) )
    {
        // If a pawn hasn't yet moved, it can move up two spaces
        coords.insert( {x, y+(2*dy)} );
    }
    
    // Pawns can only attack diagonally
    if( inBounds(x+1, y+dy) && color( board->index( x+1, y+dy ) ) == enemyColor(piece_color) )
    {
        coords.insert( {x+1, y+dy} );
    }
    if( inBounds(x-1, y+dy) && color( board->index( x-1, y+dy ) ) == enemyColor(piece_color) )
    {
        coords.insert( {x-1, y+dy} );
    }
    
    return coords;
    
}

bool Chess::check( Pieces turn, Board* board )
{
    return false;
}

bool Chess::checkMate( Pieces turn, Board* board )
{
    return false;
}

bool Chess::inBounds( int x, int y )
{
    return ( x >= 0 && x < DIMENSION && y >= 0 && y < DIMENSION );
}

std::set< std::tuple<int,int> > Chess::crawlDirection( int x, int y, int dx, int dy, std::set< std::tuple<int,int> > coords, Pieces mover_color, Board* board )
{
    if( board == NULL )
    {
        board = grid;
    }
        
    if( !inBounds(x, y) || mover_color == color( board->index(x,y) ) )
    {
        return coords;
    }
    
    coords.insert( {x, y} );
    
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