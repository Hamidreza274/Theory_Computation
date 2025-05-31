from DPDA import DPDA
from Node import Node

def intInput(first=0, end=0, f=False):
    try:
        n = int(input())
        if f and (n < first or n > end):
            raise Exception('OutOfRange')
        
    except Exception as ex:
        print(ex)
        return intInput(first, end, f)
    return n


def menu():
    print('\nplease enter the on option')
    print('1.string Member of the Language?')
    print('2.ParseTree (with stack & parseTable & lookahead)')
    print('3.ParseTree (with DPDA)')
    print('4.change variable name')
    print('5.changeGrammer')
    print('6.Exit')
        
        
while True:
    try:
        path = input('please enter the address of the file containing the grammer: ')
        dpda = DPDA(path)
        tree = None
        while True:
            menu()
            n = intInput(1, 6, True)
        
            try :
                if n == 1:
                    Node.counter = 1
                    pth = input('please enter the address of the file containing the strings: ')
                    tree = dpda.createParseTree(dpda.dpda, pth)
                    print('True') if tree else print('False')
                
                elif n == 2:
                    Node.counter = 1
                    pth = input('please enter the address of the file containing the strings: ')
                    tree = dpda.createParseTree(dpda.dpda, pth)
                    if tree: tree.PrintTree() 
                    else: raise Exception('The string is not a member of the language')
                    
                elif n == 3:
                    Node.counter = 1
                    pth = input('please enter the address of the file containing the strings: ')
                    tree = dpda.createParsingTree(pth)
                    if tree: tree.PrintTree() 
                    else: raise Exception('The string is not a member of the language')
                    
                elif n == 4:
                    print(f'Please enter the id (1-{Node.counter - 1})')
                    id = intInput(1, Node.counter, True)
                    node = tree.findNode(id)
                    if node.value not in dpda.varStr:
                        raise Exception('Only variable names can be changed.')
                    string = input('enter the new value: ')
                    tree.changeValue(id, string)
                    tree.PrintTree()
                    tree.createFile()
                    
                elif n == 5:
                    break
                
                else :
                    exit(0)
            except Exception as ex:
                print(ex)
                
    except Exception as ex:
        print(ex)