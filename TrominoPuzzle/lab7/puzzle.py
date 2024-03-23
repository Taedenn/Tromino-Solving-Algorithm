import argparse
import draw


# class of board
# every board is an object of the class Board 
class Board:
    def __init__(self, left, right, bottom, top):
        self.left, self.right, self.bottom, self.top = left, right, bottom, top

    # call this method to return four boundaries of the board 
    def get_boundary(self):
        return self.left, self.right, self.bottom, self.top


class Puzzle:
    def __init__(self, size, block):
        # size is the size of board. 
        # block is the position (x,y) of the block 

        # fill the initial block as black
        draw.draw_one_square(block, 'k')
        # draw the grid on the board 
        draw.grid(size)

        # create the board at full size 
        board = Board(1, size, 1, size)
        # call solve to fill the Tromino recursively using divide and conquer 
        self.solve(block, board)

        # show and save the result in a picture 
        draw.save_and_show(size, block)

    def solve(self, block, board):
        # block is a position (row, column) and board is an object of Board class 
        # recursively call solve() on four small size boards with only one block on each board
        # stop the recursive call when reaching to the base case, which is board 2*2
        #  
        # call draw.draw_one_tromino(type, board) to draw one type of tromino at the center of the board.
        # The type of the tromino is an integer 1 to 4 as explained in the instruction and the board is
        # an object of Board class where you want to draw the tromino at its center.

        left, right, bottom, top = board.get_boundary()
        # your code goes here:
        blocks = [block]
        tromino, square1, square2, square3 = self.get_tromino_type(block, board)
        draw.draw_one_tromino(tromino, board)

        if right - left == 1:
            return

        blocks += [square1, square2, square3]
        for square in blocks:
            quadrant = self.get_quadrant(square, board)
            match quadrant:
                case quadrant if quadrant == 1:
                    quad1 = Board((left + right + 1)//2, right, (bottom + top + 1)//2, top)
                    self.solve(square, quad1)
                case quadrant if quadrant == 2:
                    quad2 = Board(left, (left + right)//2, (bottom + top + 1)//2, top)
                    self.solve(square, quad2)
                case quadrant if quadrant == 3:
                    quad3 = Board(left, (left + right)//2, bottom, (bottom + top)//2)
                    self.solve(square, quad3)
                case quadrant if quadrant == 4:
                    quad4 = Board((left + right + 1)//2, right, bottom, (bottom + top)//2)
                    self.solve(square, quad4)

    def get_quadrant(self, block, board):
        '''
            I noticed that block is treated as (y,x) rather than (x,y), so this function determines what 'quadrant'
            the block is in by checking if block[y] is
        '''
        left, right, bottom, top = board.get_boundary()
        x, y = block[1], block[0]
        if y - bottom < top - y:
            quadrant = 3
            if x - left > right - x:
                quadrant += 1
        else:
            quadrant = 1
            if x - left < right - x:
                quadrant += 1
        return quadrant

    def get_tromino_type(self, block, board):
        # return the type of the tromino you should draw based on the position of the block and the board.
        left, right, bottom, top = board.get_boundary()
        # your code goes here:
        '''
            quadrant number corresponds with tromino type needed, in addition, this function
            will also return what squares are filled in for the recursive call. 
        '''
        quadrant = self.get_quadrant(block, board)
        square1, square2, square3 = (), (), ()
        cr, cc = (top + bottom) // 2, (right + left) // 2
        match quadrant:
            case quadrant if quadrant == 1:
                square1, square2, square3 = (cr, cc), (cr, cc + 1), (cr + 1, cc)
            case quadrant if quadrant == 2:
                square1, square2, square3 = (cr, cc), (cr, cc + 1), (cr + 1, cc + 1)
            case quadrant if quadrant == 3:
                square1, square2, square3 = (cr, cc + 1), (cr + 1, cc), (cr + 1, cc + 1)
            case quadrant if quadrant == 4:
                square1, square2, square3 = (cr, cc), (cr + 1, cc), (cr + 1, cc + 1)
        return quadrant, square1, square2, square3


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='puzzle')

    parser.add_argument('-size', dest='size', required=True, type=int, help='size of the board: 2^n')
    parser.add_argument('-block', dest='block', required=True, nargs='+', type=int,
                        help='position of the initial block')

    args = parser.parse_args()

    # size must be a positive integer 2^n
    # block must be two integers between 1 and size 
    game = Puzzle(args.size, tuple(args.block))

    # game = puzzle(8, (1,1))
    # python puzzle.py -size 8 -block 1 1
