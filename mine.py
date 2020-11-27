import random
import time

class Minesweep:

  def __init__(self, s, b):
    self.size = s
    self.bombs = set()
    self.bombCount = b
    self.pboard = [['-' for row in range(s)] for column in range(s)]
    self.gboard = [[0 for row in range(s)] for column in range(s)]
    
  def mines(self, a, b):
	  i = 0
	  while i < self.bombCount:
	    x = random.randint(0, self.size-1)
	    y = random.randint(0, self.size-1)
	    t = (x, y)
	    if t in self.bombs or t == (a, b):
	      continue
	    self.bombs.add(t)
	    self.gboard[y][x] = 'X'
	    if self.inbounds(x+1, y):
	      if self.gboard[y][x+1] != 'X':
	        self.gboard[y][x+1] += 1 # center right
	    if self.inbounds(x-1, y):
	      if self.gboard[y][x-1] != 'X':
	        self.gboard[y][x-1] += 1 # center left
	    if self.inbounds(x-1, y-1):
	      if self.gboard[y-1][x-1] != 'X':
	        self.gboard[y-1][x-1] += 1 # top left
	    if self.inbounds(x+1, y-1):
	      if self.gboard[y-1][x+1] != 'X':
	        self.gboard[y-1][x+1] += 1 # top right
	    if self.inbounds(x, y-1):
	      if self.gboard[y-1][x] != 'X':
	        self.gboard[y-1][x] += 1 # top center
	    if self.inbounds(x+1, y+1):
	      if self.gboard[y+1][x+1] != 'X':
	        self.gboard[y+1][x+1] += 1 # bottom right
	    if self.inbounds(x-1, y+1):
	      if self.gboard[y+1][x-1] != 'X':
	        self.gboard[y+1][x-1] += 1 # bottom left
	    if self.inbounds(x, y+1):
	      if self.gboard[y+1][x] != 'X':
	        self.gboard[y+1][x] += 1 # bottom center
	    i += 1

     
  def inbounds(self, x, y):
    if (x >= 0 and x < self.size) and (y >= 0 and y < self.size):
      return True
    return False

  def reveal(self, x, y):
    self.pboard[y][x] = self.gboard[y][x]
    if (x, y) in self.bombs:
      return False
    if self.gboard[y][x] == 0:
  	  if self.inbounds(x+1, y):
  	    if self.pboard[y][x+1] == '-':
  	      self.reveal(x+1, y)
  	  if self.inbounds(x-1, y):
  	    if self.pboard[y][x-1] == '-':
  	      self.reveal(x-1, y)
  	  if self.inbounds(x+1, y+1):
  	    if self.pboard[y+1][x+1] == '-':
  	      self.reveal(x+1, y+1)
  	  if self.inbounds(x+1, y-1):
  	    if self.pboard[y-1][x+1] == '-':
  	      self.reveal(x+1, y-1)
  	  if self.inbounds(x-1, y+1):
  	    if self.pboard[y+1][x-1] == '-':
  	      self.reveal(x-1, y+1)
  	  if self.inbounds(x-1, y-1):
  	    if self.pboard[y-1][x-1] == '-':
  	      self.reveal(x-1, y-1)
  	  if self.inbounds(x, y+1):
  	    if self.pboard[y+1][x] == '-':
  	      self.reveal(x, y+1)
  	  if self.inbounds(x, y-1):
  	    if self.pboard[y-1][x] == '-':
  	      self.reveal(x, y-1)
    return True

  def checkStatus(self):
    for i in range(self.size):
      for j in range(self.size):
        if self.pboard[j][i] == '-':
          if (i, j) not in self.bombs:
            return False
    return True
    
  def mark(self, x, y):
    if self.pboard[y][x] == '-':
      self.pboard[y][x] = '*'
      return True
    return False

  def displayBoard(self):
    print("")
    print("Bombs: " + str(self.bombCount))
    print("    " + "".join("{0:<3} ".format(str(i+1)) for i in range(self.size)))
    j = 1
    for row in self.pboard:
      print("{0:<3}".format(str(j)) + " |" + "| |".join(str(tile) for tile in row) + "|")
      j += 1


def play(game):
  game.displayBoard()
  first = True
  mark = False
  stime = time.time()
  
  while True:
    while True and not first:
      s = input("Reveal (R) or Mark (M) a tile?:")
      if s.lower() == 'r':
        mark = False
        break
      elif s.lower() == 'm':
        mark = True
        break
      else:
        print("Invalid input, type R or M")
    while True:
  	  x = input("X (column): ")
  	  try:
    	  x = int(x) - 1 # 0 based indexing
    	  if x >= 0 and x < game.size:
    	    break
    	  else:
    	    print("Invalid entry")
    	except ValueError:
    	  print('Invalid entry')
    while True:
  	  y = input("Y (row): ")
  	  try:
    	  y = int(y) - 1 # 0 based indexing
    	  if y >= 0 and y < game.size:
    	    break
    	  else:
    	    print("Invalid entry")
    	except ValueError:
    	  print('Invalid entry')
    	  
    if first:
  	  game.mines(x, y)
  	  first = False
  	  
    if mark:
  	  if not game.mark(x, y):
  	    print ("Cannot mark a uncovered tile")
    else:
      if not game.reveal(x, y):
      	game.displayBoard()
      	print("Game Over")
      	break
      	
    game.displayBoard()
    
    if game.checkStatus():
    	print("You WIN")
    	print("Your time is " + str(int(time.time()-stime)) + " seconds")
    	break

def main():
  while True:
    print("Welcome to MineSweeper, enter 'return' to exit on the 'select your game' prompt")
    difficulty = input("Select your game (beginner, intermediate, expert, custom, tutorial):")
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
  	    s = input("Enter your board size (integer >= 2):")
  	    try:
  	      s = int(s)
  	      if s >= 2:
  	        break
  	      else:
  	        print("Size too small")
  	    except ValueError:
  		    print('Invalid entry')
  	  while True:
  	    b = input("Enter your bomb count (integer > 0 and less than the total tiles):")
  	    try:
  	      b = int(b)
  	      if b > 0 and b < (s*s):
  	        break
  	      else:
  	        print("Invalid entry, must be less than " + str(s*s))
  	    except ValueError:
  	      print('Invalid entry')
  	  game = Minesweep(s, b)
  	  play(game)
    elif difficulty.lower() == "tutorial":
      print("")
      print("You are presented with a board of tiles. Some tiles contain mines (bombs), others don't. If you select a tile containing a bomb, you lose. If you manage to select all the tiles (without selecting any bombs) you win.")
      print("Selecting a tile which doesn't have a bomb reveals the number of neighbouring tiles containing bombs. Use this information plus some guess work to avoid the bombs.")
      print("Taking note that the neighbours to a tile are the tiles adjacent above, below, left, right, and all 4 diagonals. Tiles on the sides of the board or in a corner have fewer neighbors. The board does not wrap around the edges")
      print("")
      print("For this version, a tile is represented by '|-|' where the '-' means the tile is unrevealed and '|' is the boundary. A mine will be respresent by 'X' when revealed and one may mark a tile which will be denoted by '*'")
      t = Minesweep(4, 3)
      t.mines(2, 2)
      t.pboard = t.gboard
      t.displayBoard()
      print("The board above presents a sample 3x3 game with all tiles revealed to showcase how the number works in relation to the bombs")
      print("")
      print("Next try to complete a game on same board size to get a hang of selecting a coordinate and applying the logic with the numbers revealing neighbouring bombs")
      while True:
  	    t = Minesweep (4, 3)
  	    play(t)
  	    if t.checkStatus():
  	      print("Good job, try a harder game now")
  	      break
  	    print("Retry, sometimes luck is involved")
    elif difficulty == "":
  	  break
    else:
  	  print("Invalid game, try again")
    print("")

if __name__ == "__main__":
  main()