# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 08:07:31 2018

Tic Tac Toe Milestone Project 1

@author: vince
"""
import os #to clear in between turns
import time
    
#Simple local caching.  unboundlocalerror in joblib to be resolved if necessary.  Or, find a way to access lru_cache
cache = ''

## Game Environment
class board:
    def __init__(self, size):
        self.set_size(size)
        
    def get_size(self):
        return self.size
        
    def set_size(self, size):
        if size < 9:
            print("Boardsize too small.  Setting to 9")
            self.size = 9
        else:
            self.size = size         
        #print('A board of size ', self.size, ' has been created')
## End Game Environment


## Game Engine
class action(board):
    
    def __init__(self, size=0, player='I', move=0):
        board.__init__(self,size)
        self.move = 0
        
    def get_player(turn):
        if turn % 2 == 0:
            return 'A'
        else:
            return 'B'
        
    def get_player_icon(player):
        #Icon Table returns proper insert
        return {'A':'X','B':'O'}.get(player)
        
    def turn(self, turn, player):
    #debug movement.  replace with actual 
        run = 1
        while run == 1:
            if turn == 0:
                return 1
            else:
                #Collect User Input
                self.player = player
                print("It's Player {}'s turn".format(player))
                self.move = int(input('Enter Move 1-9 or 0 to STOP: '))
                print("validity_check ", action.valid_move(self.move))
                if action.valid_move(self.move):
                    #Clear terminal and loop
                    os.system('cls')      
                    return self.move
                else:
                    os.system('cls')
                    action.printboard(buildframe(0,0), self.size)
                    print('Invalid Move.  Try Again Player {}: '.format(player))
                
    def valid_move(move):
        if move > 9:
            return False

        global cache
        dframe = cache_parse(cache)
        if dframe[move-1] != '*':
            return False    
        return True
    
    def printboard(frame, size):
    #Print board from move lookup, including
        os.system('cls')   
        padding = int(size/6)*' '
        
        i = 0
        while i < 10:
            print()
            i += 1
            
        for row in frame[0:3]:
            templist = [] 
            padlist = []
            for mark in row:
                templist.append('|'+ padding + mark + padding + '|')
                padlist.append('|'+ padding + ' ' + padding + '|')
                
            markrow = ''.join(templist)
            padrow = ''.join(padlist) 
            print(markrow.center(75,' '))
            for i in range(len(padding)):
                print(padrow.center(75,' '))
        
    def checkwin():
        global cache
        dframe = cache_parse(cache)
        winlist = [[1,2,3],[4,5,6],[7,8,9],
                   [1,4,7],[2,5,8],[3,6,9],
                   [1,5,9],[3,5,7]]
        
        for i in range(len(winlist)):
            result_x = map(lambda x: dframe[x-1]==action.get_player_icon('A') , winlist[i])
            result_o = map(lambda x: dframe[x-1]==action.get_player_icon('B') , winlist[i])
            #Return Win Status
            if False not in list(result_x):
                print('Player A Has Won!')
                return True
            if False not in list(result_o):
                print('Player B has Won!')
                return True
        return False
    
## 'Frame' construction - drawing frames for display
def initframe():
    return 3*[3*'*']

def buildframe(player,move):
    #print('player passed to buildframe is: ', player)
    global cache
    
    #return copy of cache if move == 0
    if move == 0:
        player = cache.split(';')[3]
        move = int(cache.split(';')[4])
    
    newframe = cache_parse(cache)
    newframe[move-1] = action.get_player_icon(player)
    
    #Rebuild array
    newframe = stack_frame(newframe).copy()
    
    framestr = frametostr(newframe,player,move)
    cacheframe(framestr)
    storeframe(framestr)
    return newframe

def cache_parse(cachestr):
    newframe = []
    frame = cachestr.split(';')[0:3]
    
    #Create an easy to access 1-D list for assignment of move
    for row in frame:
        for column in row:
            newframe.append(column)
    return newframe

def stack_frame(frame):
    #make 1x3 list of lists for output/checking
    tempframe = 3*[3*[]]
    tempframe[0] = ''.join(frame[0:3])
    tempframe[1] = ''.join(frame[3:6])
    tempframe[2] = ''.join(frame[6:])    
    return tempframe



## End Game Engine    

## The following functions manage frame storage for calling
def cacheframe(framestr):
    global cache
    cache = framestr
    #print('Cached the following string: ', cache)

    # Convert frame and move to string
def frametostr(frame,player,move):
    frame.extend([str(player),str(move)])
    #print('frame to turn into string: ', frame)
    cachestr = ';'.join(frame)
    return cachestr
    
    # Write frame and turn information to file
def storeframe(framestr):
    f = open("gamerecord.txt", "a+")
    writestr = framestr + ';' + str(time.time()) + '\n'
    f.write(writestr)
    f.close

## End storage management


## Get things started by caching an empty frame and taking in the total board size to be displayed
def startgame():
    #get an empty frame and cache it, then begin storing data.
    framestr = frametostr(initframe(),'I',0)
    cacheframe(framestr)
    storeframe(framestr)
    #Intro Sequence
    print('Welcome to TicTacToe!'.center(30,' '))
    return int(input('How big would you like the board?: '))
## End game initialization

#Using main as the handler to keep fields up to date
def main():
    
    field = board(startgame())
    newturn = action(field.get_size(), 'I', 0)
    #Run Game
    turnnum = 0
    move = 1
    while move:

        #Print Empty Board
        if turnnum == 0:
            action.printboard(initframe(),field.size)
            print('Lets Begin!')
        else:
            #Get next move
            move = action.turn(newturn,turnnum,action.get_player(turnnum))
            
            #Build and print the new frame
            if move == 0:
                break
            action.printboard(buildframe(action.get_player(turnnum),move),newturn.size)
            
            if action.checkwin():
                repeat = input("Play Another? (Y/N) ").lower()
                if repeat == 'y':
                    main()
                move = False
                
        turnnum += 1
        
if __name__ == '__main__':
     main()
     
     
     
     