import numpy as np
import random
import copy
import time

class Board:
    def __init__(self):
        # Parameters:config, white, black
        config = np.zeros((8,8))   # Empty = 0
        config[0:2] = 2*np.ones((2,8))  # Black = 2
        config[6:8] = np.ones((2,8))    # White = 1
        self.config = config
        self.workers = []
        white = []
        black = []
        for i in range(8):
            white.append((6,i))
            white.append((7,i))
            black.append((0,i))
            black.append((1,i))
        self.workers = [white,black]
        return

    def readboard(self,filename):
        self.config = np.zeros((8,8))
        white = []
        black = []
        temp = []
        with open(filename,"r") as fp:
            for line in fp:
                temp.append(list(line))
        fp.close()
        for i in range(8):
            for j in range(8):
                if temp[i][j] == '_':
                    self.config[(i,j)] = 0
                elif temp[i][j] == 'b':
                    self.config[(i,j)] = 2
                    black.append((i,j))
                elif temp[i][j] == 'w':
                    self.config[(i,j)] = 1
                    white.append((i,j))
        self.workers = [white,black]
        return

    def hasfinished(self):
        # Returns {0, 1, 2} = {not finished, white wins, black wins}
        if len(self.workers[0]) == 0:
            return 2
        if len(self.workers[1]) == 0:
            return 1
        for i in range(8):
            if self.config[0,i]==1:
                return 1
            if self.config[7,i]==2:
                return 2
        return 0

    def printboard(self):
        # Print the board
        for i in range(8):
            b = []
            for j in range(8):
                if self.config[i,j] == 0:
                    b += ['_']
                elif self.config[i,j] == 1:
                    b += ['w']
                elif self.config[i,j] == 2:
                    b += ['b']
            print(''.join(b))
        print()
        print('White workers:')
        print(self.workers[0])
        print('Black workers:')
        print(self.workers[1])
        print()
        return

    def canMove(self,pos,dir):
        # dir = {0,1,2} = {forward left, forward, forward right}
        # return {0,1,2} = {cannot move, can move no capture, can move with capture}
        config = self.config
        if config[pos] == 0:
            print('Position is empty!')
            return 0
        if config[pos] == 1:
            if dir==0 and pos[0]>0 and pos[1]>0:
                if config[(pos[0]-1,pos[1]-1)]==0:
                    return 1
                elif config[(pos[0]-1,pos[1]-1)]==2:
                    return 2
            elif dir==1 and pos[0]>0:
                if config[(pos[0]-1,pos[1])]==0:
                    return 1
                elif config[(pos[0]-1,pos[1])]==2:
                    return 0
            elif dir==2 and pos[0]>0 and pos[1]<7:
                if config[(pos[0]-1,pos[1]+1)]==0:
                    return 1
                elif config[(pos[0]-1,pos[1]+1)]==2:
                    return 2
        elif config[pos] == 2:
            if dir==0 and pos[0]<7 and pos[1]<7:
                if config[(pos[0]+1,pos[1]+1)]==0:
                    return 1
                elif config[(pos[0]+1,pos[1]+1)]==1:
                    return 2
            elif dir==1 and pos[0]<7:
                if config[(pos[0]+1,pos[1])]==0:
                    return 1
                elif config[(pos[0]+1,pos[1])]==1:
                    return 0
            elif dir==2 and pos[0]<7 and pos[1]>0:
                if config[(pos[0]+1,pos[1]-1)]==0:
                    return 1
                elif config[(pos[0]+1,pos[1]-1)]==1:
                    return 2
        return 0

    def move(self,pos,dir):
        # NOT checking whether can move
        if self.config[pos] == 0:
            print('Nothing to Move!')
            return
        elif self.config[pos] == 1:
            if dir==0:
                if self.config[(pos[0]-1,pos[1]-1)] == 2:
                    self.workers[1].remove((pos[0]-1,pos[1]-1))
                self.config[(pos[0]-1,pos[1]-1)] = 1
                self.workers[0].append((pos[0]-1,pos[1]-1))
            elif dir==1:
                self.config[(pos[0]-1,pos[1])] = 1
                self.workers[0].append((pos[0]-1,pos[1]))
            elif dir==2:
                if self.config[(pos[0]-1,pos[1]+1)] == 2:
                    self.workers[1].remove((pos[0]-1,pos[1]+1))
                self.workers[0].append((pos[0]-1,pos[1]+1))
                self.config[(pos[0]-1,pos[1]+1)] = 1
            self.workers[0].remove(pos)

        elif self.config[pos] == 2:
            if dir==0:
                if self.config[(pos[0]+1,pos[1]+1)] == 1:
                    self.workers[0].remove((pos[0]+1,pos[1]+1))
                self.config[(pos[0]+1,pos[1]+1)] = 2
                self.workers[1].append((pos[0]+1,pos[1]+1))
            elif dir==1:
                self.config[(pos[0]+1,pos[1])] = 2
                self.workers[1].append((pos[0]+1,pos[1]))
            elif dir==2:
                if self.config[(pos[0]+1,pos[1]-1)] == 1:
                    self.workers[0].remove((pos[0]+1,pos[1]-1))
                self.config[(pos[0]+1,pos[1]-1)] = 2
                self.workers[1].append((pos[0]+1,pos[1]-1))
            self.workers[1].remove(pos)
        self.config[pos] = 0
        return

    # Heuristics
    def dh1(self,color):
        return 2*len(self.workers[color-1]) + random.random()
    def oh1(self,color):
        return 2*(30-len(self.workers[2-color])) + random.random()

# Search Strategies
def minmax(board,depth,color,Max=True):
    if depth==0 or board.hasfinished()>0:
        return (board.dh1(color),((-1,-1),-1))
    if Max:
      strategy = ((-1,-1),-1)
      value = float('-inf')
      for w in board.workers[color-1]:
          for dir in range(3):
              if board.canMove(w,dir)>0:
                  newboard = copy.deepcopy(board)
                  newboard.move(w,dir)
                  temp=minmax(newboard,depth-1,color,False)
                  curval=temp[0]
                  if value < curval:
                      value = curval
                      strategy = (w,dir)
    else:
      strategy = ((-1,-1),-1)
      value=float('inf')
      for w in board.workers[2-color]:
          for dir in range(3):
              if board.canMove(w,dir)>0:
                  newboard = copy.deepcopy(board)
                  newboard.move(w,dir)
                  temp=minmax(newboard,depth-1,color,True)
                  curval=temp[0]
                  if value > curval:
                      value = curval
                      strategy = (w,dir)
    return (value,strategy)


# Search Strategies
def minmax2(board,depth,color,Max=True):
    if depth==0 or board.hasfinished()>0:
        return (board.oh1(color),((-1,-1),-1))
    if Max:
      strategy = ((-1,-1),-1) #White
      value = float('-inf')
      for w in board.workers[color-1]:
        for dir in range(3):
          if board.canMove(w,dir)>0:
            newboard = copy.deepcopy(board)
            newboard.move(w,dir)
            temp=minmax2(newboard,depth-1,color,False)
            curval=temp[0]
            if value < curval:
              value = curval
              strategy = (w,dir)
    else:  # Black
      strategy = ((-1,-1),-1)
      value=float('inf')
      for w in board.workers[2-color]:
        for dir in range(3):
          if board.canMove(w,dir)>0:
            newboard = copy.deepcopy(board)
            newboard.move(w,dir)
            temp=minmax2(newboard,depth-1,color,True)
            curval=temp[0]
            if value > curval:
              value = curval
              strategy = (w,dir)
    return (value,strategy)

def ab(board,depth,color,a,b,Max=True): 
    if depth==0 or board.hasfinished()>0:
        return (board.oh1(color),((-1,-1),-1))
    if Max:
      strategy = ((-1,-1),-1) #White
      for w in board.workers[color-1]:
        for dir in range(3):
          if board.canMove(w,dir)>0:
            newboard = copy.deepcopy(board)
            newboard.move(w,dir)
            temp=ab(newboard,depth-1,color,a,b,False)
            curval=temp[0]
            if a < curval:
              a = curval
              strategy = (w,dir)
            if a >= b:
              return (a,strategy)
      return (a, strategy)
    else:  # Black
      strategy = ((-1,-1),-1)
      for w in board.workers[2-color]:
        for dir in range(3):
          if board.canMove(w,dir)>0:
            newboard = copy.deepcopy(board)
            newboard.move(w,dir)
            temp=ab(newboard,depth-1,color,a,b,True)
            curval=temp[0]
            if b > curval:
                b = curval
                strategy = (w,dir)
            if a >= b:
              return (b,strategy)
      return (b,strategy)

def alphabeta(board,depth,color,a,b,reftab,Max=True):    # initialize a=neginf b=posinf
    if depth==0 or board.hasfinished()>0:
        return (board.oh1(color),((-1,-1),-1))
    rt = []
    if Max:
      # Want larger in front
      strategy = ((-1,-1),-1)
      # Construct Search table
      searchlist = []
      for w in board.workers[color-1]:
          for dir in range(3):
              searchlist.append((w,dir))
      # Search refutable table first
      for strat in reftab:
          w = strat[0]
          dir = strat[1]
          if w in board.workers[0] and board.canMove(w,dir):
              searchlist.remove(strat)
              newboard = copy.deepcopy(board)
              newboard.move(w,dir)
              temp=alphabeta(newboard,depth-1,color,a,b,rt,False)
              curval=temp[0]
              if a < curval:
                  a = curval
                  strategy = (w,dir)
              if a >= b:
                  return (a,strategy)
      # Regular search
      for strat in searchlist:
          w = strat[0]
          dir = strat[1]
          if board.canMove(w,dir)>0:
              newboard = copy.deepcopy(board)
              newboard.move(w,dir)
              temp=alphabeta(newboard,depth-1,color,a,b,rt,False)
              curval=temp[0]
              if a < curval:
                  a = curval
                  strategy = (w,dir)
              if a >= b:
                  # Record into refutable table for future reference
                  reftab.append(strategy)
                  #print(len(reftab))
                  return (a,strategy)
      return (a,strategy)
    else:
      # Want smaller in front
      strategy = ((-1,-1),-1)
      # Construct Search table
      searchlist = []
      for w in board.workers[2-color]:
          for dir in range(3):
              searchlist.append((w,dir))
      # Refutable table first
      for strat in reftab:
          w = strat[0]
          dir = strat[1]
          if w in board.workers[1] and board.canMove(w,dir):
              searchlist.remove(strat)
              newboard = copy.deepcopy(board)
              newboard.move(w,dir)
              temp=alphabeta(newboard,depth-1,color,a,b,rt,True)
              curval=temp[0]
              if b > curval:
                  b = curval
                  strategy = (w,dir)
              if a >= b:
                  return (b,strategy)
      # Regular
      for strat in searchlist:
          w = strat[0]
          dir = strat[1]
          if board.canMove(w,dir)>0:
              newboard = copy.deepcopy(board)
              newboard.move(w,dir)
              temp=alphabeta(newboard,depth-1,color,a,b,rt,True)
              curval=temp[0]
              if b > curval:
                  b = curval
                  strategy = (w,dir)
              if a >= b:
                  reftab.append(strategy)
                  #print(len(reftab))
                  return (b,strategy)
      return (b,strategy)


def play(board):
    while True:
        start = time.time()
        #s=alphabeta(board,5,1,float('-inf'),float('inf'),[])[1]
        s=ab(board,5,1,float('-inf'),float('inf'))[1]
        print(time.time()-start)
        board.printboard()
        board.move(s[0],s[1])
        if board.hasfinished() == 1:
            board.printboard()
            print("white wins")
            print()
            break
        board.printboard()
        s=minmax2(board,3,2)[1]
        board.printboard()
        board.move(s[0],s[1])
        if board.hasfinished()== 2:
            board.printboard()
            print("black wins")
            print()
            break
        board.printboard()



b = Board()
# b.readboard("error.txt")
play(b)
