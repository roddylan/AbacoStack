# AbacoStack.py
# Roderick Lan - 1706751
# Contains all necessary classes


import random

class Card: # card u want to make
    def __init__(self,width,depth): #width = colors
        self._beads = [] #list storing in order the beads in each stack, starting with the first stack to the last, each stack stored top to bottom.
        self.width = int(width)
        self.depth = int(depth)
        # fill beads list
        for i in range(self.width):
            for __ in range(self.depth):
                self._beads.append(chr(ord('A')+i))
        self.reset()
        
    
    def reset(self):
        '''
        Shuffle/reshuffle the card and generate a new configuration
        Input: None
        Return: None
        '''
        random.shuffle(self._beads)
        
    
    def show(self):
        '''
        Display the card
        Input: None
        Return: None
        '''
        for i in range(self.depth):
            temp = ''
            for j in range(self.width):
                temp = temp+' '+self._beads[i+j*self.depth]
            temp = temp.strip(' ')
            temp = '|'+temp+'|'
            print(temp)
                
        
    
    def stack(self,number):
        '''
        Return the ordered list of elements top to bottom in the given stack
        Input: Stack number
        Return: List of elements in given stack
        '''
        #assert number <= self.width, 'Stack number exceeds number of stacks'
        #assert number > 0, 'Stack number too low'
        if number > self.width or number <= 0:
            raise Exception('Error: Invalid Stack Number')
        
        start = (number-1)*self.depth
        end = start+self.depth
        return self._beads[start:end]

    
    def __str__(self):
        '''
        Return a string expression of class
        Input: None
        Return: String expression
        '''
        string = ''
        for i in range(self.width):
            string = string+'|'
            for j in range(self.depth):
                string = string+self._beads[i*self.depth+j]
            string = string+'|'
        return string
    
    
    def replace(self,filename,n):
        '''
        Replace card state with new configuration from a given line in the file
        Input: filename, index of line
        Return: None
        '''
        if not filename[-4:] == '.txt':
            raise Exception('Error: Invalid Filename')
        
        file = open(filename)
        contents = file.readlines()
        file.close()
        self._beads = contents[n].strip(' \n').split(' ')
        #print(self._beads)
        
        
        colors = []
        for item in self._beads:
            if item not in colors:
                colors.append(item)
        self.width = len(colors)
        self.depth = self._beads.count(colors[0])
        #print('w:',self.width,'d:',self.depth)
        
class BStack:
    def __init__(self,capacity):
        assert isinstance(capacity,int), 'Error: Type Error: %s' % (type(capacity))
        assert capacity >= 0, 'Error: Illegal Capacity: %d' % (capacity)
        
        self.items = []
        self.capacity = capacity
    
    def push(self,item):
        '''
        Push item onto stack
        Input: item that will be added
        Return: None
        '''
        if self.isFull():
            raise Exception('Error: BoundedStack is Full')
        
        self.items.append(item)
        
    
    def pop(self):
        '''
        Pop/remove item from stack
        Input: None
        Return: Popped item
        '''
        if self.isEmpty():
            raise Exception('Error: BoundedStack is Empty')
        
        return self.items.pop()
    
    def peek(self):
        '''
        Returns the top item from the stack but doesn't remove it
        Input: None
        Return: Top item in stack
        '''
        if self.isEmpty():
            raise Exception('Error: BoundedStack is Empty')
        
        return self.items[-1]
        
    
    def isEmpty(self):
        '''
        Check if stack is empty
        Input: None
        Return: bool (True if empty, False if not)
        '''
        return self.items == []
        
    
    def isFull(self):
        '''
        Check if stack is full
        Input: None
        Return: bool (True if full, False if not)
        '''
        return self.size() >= self.capacity
        
    
    def size(self):
        '''
        Return the number of items in the stack
        Input: None
        Return: Size of stack
        '''
        return len(self.items)


    def reset(self):
        '''
        Reset/empty the stack
        Input: None
        Return: None
        '''
        self.items = []
        
    
    def __str__(self):
        '''
        Return a string representation of class
        Input: None
        Return: String representation
        '''
        string = ''
        for item in self.items:
            string += item#+' '
        #string = string.strip(' ')
        return string




class AbacoStack:
    def __init__(self, stacks, depth):
        #size of toprow
        self.size = stacks + 2
        
        self.depth = depth
        
        self.stacks = []
        self.toprow = ['.']*self.size
        
        self.moves = 0
        
        # populate list of stacks
        for i in range(stacks):
            temp = BStack(self.depth)
            for __ in range(self.depth):
                temp.push(chr(ord('A')+i))
            self.stacks.append(temp)
        
        
        
    def moveBead(self, move):
        '''
        Changes the state of AbacoStack instance based on valid moves. Exception raised if move is invalid. Update total number of moves made.
        Input: 2 character string representing user's move
        Return: None
        '''
        if len(move) != 2:
            raise Exception('Error: Invalid Move')
        
        position = int(move[0])
        direction = move[1].lower()
        
        if position >= len(self.toprow):
            raise Exception('Error: Invalid Move')
        
        if direction == 'd':
            if self.stacks[position-1].isFull() or self.toprow[position] == '.':
                raise Exception('Error: Invalid Move')
            self.stacks[position-1].push(self.toprow[position])
            self.toprow[position] = '.'
        
        if direction == 'u':
            if position == 0 or position == len(self.toprow)-1 or self.stacks[position-1].isEmpty() or self.toprow[position] != '.':
                raise Exception('Error: Invalid Move')
            self.toprow[position] = str(self.stacks[position-1].pop())
        
        if direction == 'r':
            if position == len(self.toprow)-1 or self.toprow[position+1] != '.' or self.toprow[position] == '.':
                raise Exception('Error: Invalid Move')
            else:
                self.toprow[position+1] = self.toprow[position]
                self.toprow[position] = '.'
                
        if direction == 'l':
            if position == 0 or self.toprow[position-1] != '.' or self.toprow[position] == '.':
                raise Exception('Error: Invalid Move')
            else:
                self.toprow[position-1] = self.toprow[position]
                self.toprow[position] = '.'
        self.moves += 1
        
        # 1u means stack 1 upward move
        # 1d means stack 1 downward move
        # 2u means stack 2 upward move
        # 2d means stack 2 downward move
        # 3u means stack 3 upward move
        # 3d means stack 3 downward move
        # 0r means position 0 right move
        # 1r and 1l mean position 1 right move and left move respectively
        # 2r and 2l mean position 2 right move and left move respectively
        # 3r and 3l mean position 3 right move and left move respectively
        # 4l means position 4 left move
        
        
    
    def isSolved(self, card):
        '''
        Check if AbacoStack and card are same (AbacoStack solved)
        Input: instance of card class
        Return: bool (True if solved, False if not)
        '''
        # loop through stacks
        for i in range(len(self.stacks)):
            # loop through number of items per stack
            for j in range(self.depth):
                # check if AbacoStack is not solved
                if len(str(self.stacks[i])) < self.depth:
                    return False
                if card.stack(i+1)[j] != str(self.stacks[i])[j]:
                    return False
        return True
            
        
    
    def reset(self):
        '''
        Reset the number of moves and AbacoStack to initial position
        Input: None
        Return: None
        '''
        self.moves = 0
        self.stacks = []
        self.toprow = ['.']*self.size
        
        #loop through num of stacks
        for i in range(self.size-2):
            #fill stacks with same letter
            temp = BStack(self.depth)
            for __ in range(self.depth):
                temp.push(chr(ord('A')+i))
            self.stacks.append(temp)        
        #pass
    
    def show(self,card=None):
        '''
        Display AbacoStack and card (optional)
        Input: instance of card class (optional)
        Return: None
        '''
        lines = ['','']
        
        # set first 2 lines 
        for i in range(len(self.toprow)):
            lines[0] += str(i) + ' '
            lines[1] += self.toprow[i] + ' '
        
        if card:
            lines[1] = f"{lines[1]}{'card':>{8+len(self.stacks)//2}}"
        
        # loop through depth of stacks 
        # reversed to account for location of bottom/top of stack
        for i in reversed(range(self.depth)):
            line = '| '
            for item in self.stacks:
                if i >= item.size():
                    line += '. '
                else:
                    line += str(item)[i] +' '
            line +='|'
            
            if card:
                line = f"{line}{'|':>5}"
                
                for j in range(len(self.stacks)):
                    line += card.stack(j+1)[i] + ' '
                # get rid of extra spaces
                line = line.strip(' ')
                
                line += '|'
                
            lines.append(line)
        
        # bottom border of AbacoStack
        lastline = f"{'+':-<{len(lines[0])-2}}+"
        if card:
            # add number of moves made to final line
            lastline = f"{lastline}{self.moves:>{8+len(self.stacks)+4}} moves"
        lines.append(lastline)
        
        #print all lines
        for l in lines:
            print(l)
        
        
    

def TestCard():
    # test Card class
    a = Card(3,3) 
    a.show()
    print('new card:')
    a.reset()
    a.show()
    print(a.stack(1))
    print(a.stack(2))
    print(a.stack(3))
    
    try:
        print('check invalid stack:')
        print(a.stack(4))
    except Exception as e:
        print(e)
    
    print(a)
    
    try:
        print('replaced -------------------')
        a.replace('test.txt',0)
        print(a)
        a.show()
        print('replaced -------------------')
        a.replace('test.txt',1)
        print(a)
        a.show()
    except Exception as e:
        print(e)    
    

def TestBoundedStack():
    # Test BStack class
    bs = BStack(3)
    print('empty?',bs.isEmpty())
    print('try pop:')
    try:
        bs.pop()
    except Exception as e:
        print(e)
    print('test push')
    bs.push('1')
    bs.push('2')
    print('stack:', bs)
    print('test peek')
    print(bs.peek())
    print('stack:', bs)
    
    print('test push past capacity')
    try:
        bs.push('3')
        bs.push('4')
    except Exception as e:
        print(e)
    print('stack:', bs)
    print('full?',bs.isFull())


def TestAbacoStack():
    # test AbacoStack class
    a = AbacoStack(3,3)
    try:
        a.moveBead('1d')
    except Exception as e:
        print(e)
    
    try:
        a.moveBead('4r')
    except Exception as e:
        print(e)
    
    
    c = Card(3,3)
    a.show(c)
    a.moveBead('1u')
    a.show()
    a.moveBead('1r')
    a.show()
    a.moveBead('2r')
    a.show()
    a.moveBead('2u')
    a.show()
    a.moveBead('2l')
    a.show()
    a.moveBead('1d')
    a.show()
    a.moveBead('3l')
    a.show()
    a.moveBead('2d')
    a.show()
    
    print(a.stacks[0])
    print(c.stack(1))
    
    a.show(c)
    
    print('solved?',a.isSolved(c))
    
    #c.replace('test.txt',2)
    a.show(c)
    print('solved?',a.isSolved(c))
    try:
        a.moveBead('1u 1l 2u 3u 3u')
    except Exception as e:
        print(e)
    finally:
        a.show(c)
        
    print('reset:')
    a.reset()
    a.show(c)

def main():
    # test card
    print('CARD TEST:')
    TestCard()
    # test BStack
    print('BOUNDEDSTACK TEST:')
    TestBoundedStack()
    
    # test AbacoStack
    print('ABACOSTACK TEST:') 
    TestAbacoStack()

    
    
if __name__ == '__main__':
    main()