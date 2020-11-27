import random
import time


# Class contianing all data relevant to the game

class Minesweep:

  # Initialize the class with the size of the game (always a square) and the number of bombs

    def __init__(self, s, b):
        self.size = s
        self.bombs = set()
        self.bombCount = b
        self.pboard = [['-' for row in range(s)] for column in range(s)]  # initialize the board the player views
        self.gboard = [[0 for row in range(s)] for column in range(s)]  # initialize the board the game uses

  # Function for setting up the game board randomly with mine, noting a bomb cannot be under the players first move

    def mines(self, a, b):

        i = 0

        while i < self.bombCount:  # place as many bombs as requested
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            t = (x, y)

            if t in self.bombs or t == (a, b):  # make sure we dont double up bombs on the same coordinate or place one under the first move
                continue

            self.bombs.add(t)
            self.gboard[y][x] = 'X'

        # Increase every the bomb neighbours' number by one, if they exist on the board and are not a bomb

            if self.inbounds(x + 1, y):
                if self.gboard[y][x + 1] != 'X':
                    self.gboard[y][x + 1] += 1  # center right neighbour
            if self.inbounds(x - 1, y):
                if self.gboard[y][x - 1] != 'X':
                    self.gboard[y][x - 1] += 1  # center left neighbour
            if self.inbounds(x - 1, y - 1):
                if self.gboard[y - 1][x - 1] != 'X':
                    self.gboard[y - 1][x - 1] += 1  # top left neighbour
            if self.inbounds(x + 1, y - 1):
                if self.gboard[y - 1][x + 1] != 'X':
                    self.gboard[y - 1][x + 1] += 1  # top right neighbour
            if self.inbounds(x, y - 1):
                if self.gboard[y - 1][x] != 'X':
                    self.gboard[y - 1][x] += 1  # top center neighbour
            if self.inbounds(x + 1, y + 1):
                if self.gboard[y + 1][x + 1] != 'X':
                    self.gboard[y + 1][x + 1] += 1  # bottom right neighbour
            if self.inbounds(x - 1, y + 1):
                if self.gboard[y + 1][x - 1] != 'X':
                    self.gboard[y + 1][x - 1] += 1  # bottom left neighbour
            if self.inbounds(x, y + 1):
                if self.gboard[y + 1][x] != 'X':
                    self.gboard[y + 1][x] += 1  # bottom center neighbour
            i += 1

  # Function to check if a coordinate given is within the bounds of the board

    def inbounds(self, x, y):
        if x >= 0 and x < self.size and y >= 0 and y < self.size:
            return True
        return False

  # Function to reveal a tile to the player, recursively do so to the tiles neighbours if the tile has no neighbouring bombs

    def reveal(self, x, y):
        self.pboard[y][x] = self.gboard[y][x]

        if (x, y) in self.bombs:
            return False

    # Check to see if recusion is required and subsequential checks for neighbours

        if self.gboard[y][x] == 0:
            if self.inbounds(x + 1, y):
                if self.pboard[y][x + 1] == '-':
                    self.reveal(x + 1, y)
            if self.inbounds(x - 1, y):
                if self.pboard[y][x - 1] == '-':
                    self.reveal(x - 1, y)
            if self.inbounds(x + 1, y + 1):
                if self.pboard[y + 1][x + 1] == '-':
                    self.reveal(x + 1, y + 1)
            if self.inbounds(x + 1, y - 1):
                if self.pboard[y - 1][x + 1] == '-':
                    self.reveal(x + 1, y - 1)
            if self.inbounds(x - 1, y + 1):
                if self.pboard[y + 1][x - 1] == '-':
                    self.reveal(x - 1, y + 1)
            if self.inbounds(x - 1, y - 1):
                if self.pboard[y - 1][x - 1] == '-':
                    self.reveal(x - 1, y - 1)
            if self.inbounds(x, y + 1):
                if self.pboard[y + 1][x] == '-':
                    self.reveal(x, y + 1)
            if self.inbounds(x, y - 1):
                if self.pboard[y - 1][x] == '-':
                    self.reveal(x, y - 1)
        return True

  # Function to check if the game has been won by the player, comparing the game board and player's board

    def checkStatus(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.pboard[j][i] == '-':
                    if (i, j) not in self.bombs:
                        return False
        return True

  # Function that allows the player to mark an unrevealed tile

    def mark(self, x, y):
        if self.pboard[y][x] == '-':
            self.pboard[y][x] = '*'
            return True
        return False

  # Function to display the players board via the command line

    def displayBoard(self):
        print('')
        print('Bombs: ' + str(self.bombCount))
        print('    ' + ''.join('{0:<3} '.format(str(i + 1)) for i in range(self.size)))
        j = 1
        for row in self.pboard:
            print('{0:<3}'.format(str(j)) + ' |' + '| |'.join(str(tile) for tile in row) + '|')
            j += 1


# Function that controls the UI for the player while player the game

def play(game):

    game.displayBoard()
    first = True
    mark = False
    stime = time.time()

    while True:  # input handling for whether the player wants to reveal or mark a tile
        while True and not first:
            s = input('Reveal (R) or Mark (M) a tile?:')
            if s.lower() == 'r':
                mark = False
                break
            elif s.lower() == 'm':
                mark = True
                break
            else:
                print('Invalid input, type R or M')

        print('Enter the coordinates of a tile to mark/reveal:')

        while True:  # input handling for the first coordinate (x) of the tile
            x = input('X (column): ')
            try:
                x = int(x) - 1
                if x >= 0 and x < game.size:
                    break
                else:
                    print('Outside game bounds')
            except ValueError:
                print('Invalid entry')

        while True:  # input handling for the second coordinate (y) of the tile
            y = input('Y (row): ')
            try:
                y = int(y) - 1
                if y >= 0 and y < game.size:
                    break
                else:
                    print('Outside game bounds')
            except ValueError:
                print('Invalid entry')

        if first:  # if it is the first move, generate the game board with their first move entered
            game.mines(x, y)
            first = False

      # send the coordinates to the Minesweep class based one whether they choose to mark or reveal a tile

        if mark:
            if not game.mark(x, y):
                print('Cannot mark a uncovered tile')
        else:
            if not game.reveal(x, y):  # if they hit a bomb they lose
                game.displayBoard()
                print('Game Over')
                break

        game.displayBoard()

        if game.checkStatus():  # lastly check if all tiles but bombs have been revealed, if so they win
            print('You WIN')
            print('Your time is ' + str(int(time.time() - stime)) + ' seconds')
            break


# Main function to greet the player and provide options for the difficulty of the game

def main():

    while True:
        print("Welcome to MineSweeper, enter 'return' to exit on the 'select your game' prompt")
        difficulty = input('Select your game (beginner, intermediate, expert, custom, tutorial):')

        if difficulty.lower() == 'beginner':
            s = 9
            b = 10
            game = Minesweep(s, b)
            play(game)
        elif difficulty.lower() == 'intermediate':

            s = 16
            b = 40
            game = Minesweep(s, b)
            play(game)
        elif difficulty.lower() == 'expert':

            s = 22
            b = 100
            game = Minesweep(s, b)
            play(game)
        elif difficulty.lower() == 'custom':

            while True:
                s = input('Enter your board size (integer >= 2):')
                try:
                    s = int(s)
                    if s >= 2:
                        break
                    else:
                        print('Size too small')
                except ValueError:
                    print('Invalid entry')
            while True:
                b = input('Enter your bomb count (integer > 0 and less than the total tiles):')
                try:
                    b = int(b)
                    if b > 0 and b < s * s:
                        break
                    else:
                        print('Invalid entry, must be less than '+ str(s * s))
                except ValueError:
                    print('Invalid entry')
            game = Minesweep(s, b)
            play(game)
        elif difficulty.lower() == 'tutorial':

            print('')
            print("You are presented with a board of tiles. Some tiles contain mines (bombs), others don't. If you select a tile containing a bomb, you lose. If you manage to select all the tiles (without selecting any bombs) you win.")
            print("Selecting a tile which doesn't have a bomb reveals the number of neighbouring tiles containing bombs. Use this information plus some guess work to avoid the bombs.")
            print('Taking note that the neighbours to a tile are the tiles adjacent above, below, left, right, and all 4 diagonals. Tiles on the sides of the board or in a corner have fewer neighbors. The board does not wrap around the edges')
            print('You may choose to reveal or mark a tile, marking does nothing but give a visual reference to the player where they believe a bomb may be. This is useful for harder difficulties where one must track multiple bombss in an area.')
            print('')
            print("For this version, a tile is represented by '|-|' where the '-' means the tile is unrevealed and '|' is the boundary. A mine will be respresent by 'X' when revealed and a marked tile will be denoted by '*'")
            t = Minesweep(4, 3)
            t.mines(2, 2)
            t.pboard = t.gboard
            t.displayBoard()
            print('The board above presents a sample 3x3 game with all tiles revealed to showcase how the number works in relation to the bombs')
            print('')
            print('Next try to complete a game on same board size to get a hang of selecting a coordinate and applying the logic with the numbers revealing neighbouring bombs')
            while True:
                t = Minesweep(4, 3)
                play(t)
                if t.checkStatus():
                    print('Good job, try a harder game now')
                    break
                print('Retry, sometimes luck is involved')
        elif difficulty == '':

            break
        else:

            print('Invalid game, try again')

        print('')


if __name__ == '__main__':
    main()
