# main.py
# Plays AbacoStack game using AbacoStack and Card class 

from AbacoStack import AbacoStack
from AbacoStack import Card

import random


def getDimensions():
    '''
    Get dimensions/size of AbacoStack from user
    Input: None
    Return: list of dimensions [width,depth]
    '''
    validWidth = False
    validDepth = False
    while not validWidth:
        try:
            width = input('Enter the number of stacks you want the AbacoStack to have (2-5): ')
            if not width.isnumeric() or int(width) < 2 or int(width) > 5:
                # handle invalid input
                raise Exception('Error: Invalid width, please enter a number between 2 and 5')
        except Exception as e:
            print(e)
        else:
            validWidth = True
            while not validDepth:
                try:
                    depth = input('Enter the depth of stacks in the AbacoStack (2-4): ')
                    if not depth.isnumeric() or int(depth) < 2 or int(depth) > 4:
                        # handle invalid input
                        raise Exception('Error: Invalid depth, please enter a number between 2 and 4')
                except Exception as e:
                    print(e)
                else:
                    validDepth = True
                    return [int(width),int(depth)]

def getAbacoStack(width,depth):
    '''
    Get instance of AbacoStack
    Input: width, depth
    Return: AbacoStack instance
    '''
    return AbacoStack(width,depth)

def getCard(width,depth):
    '''
    Get instance of Card
    Input: width, depth
    Return: Card instance
    '''    
    return Card(width,depth)

def move(stack,moves,card):
    '''
    Deal with up to 5 moves from user. 
    Input: instance of AbacoStack, moves from user, instance of Card
    Return: bool (True if any move led to win) or None
    '''
    try:
        moves = moves.strip(' ')
        if moves == 'r':
            stack.reset()
        else:
            moves = moves.split(' ')
            for move in moves[:5]:
                stack.moveBead(move)
                if checkWin(stack,card):
                    return True
                    
    # handle invalid moves
    except Exception as e:
        print(e)
    finally:
        # display results of moves
        stack.show(card)
        #return checkWin(stack,card)
    

def checkWin(stack,card):
    '''
    Check if game is won
    Input: instance of AbacoStack, instance of Card
    Return: bool (True if AbacoStack solved, False if not)
    '''
    if stack.isSolved(card):
        return True
    else:
        return False


def main():
    continueGame = True
    gameWon = False
    while continueGame:
        dimensions = getDimensions()
        
        stack = getAbacoStack(dimensions[0],dimensions[1])
        
        card = getCard(dimensions[0],dimensions[1])
        
        while checkWin(stack,card):
            card.reset()
        
        
        stack.show(card)
        
        while not gameWon and continueGame:
            moves = input('Enter your move(s) [Q for quit and R to reset]: ').lower()
            if moves.strip(' ') == 'q':
                continueGame = False
            else:
                if move(stack,moves,card):
                    gameWon = True
                    print('Congratulations! You Win!')
                    stack.show(card)                    
        if gameWon:
            response = input('Would you like to get another configuration card attempt? (Y/N): ').lower()
            # handle input
            if response == 'y':
                gameWon = False
            elif response == 'n':
                continueGame = False
            else:
                print('Error: Invalid Response')
        
            
    


main()
