from DPDA import DPDA

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
    path = input('please enter the address of the file containing the grammer: ')
    dpda = DPDA(path)
    tree = None
    while True:
        menu()
        n = intInput(1, 6, True)
        
        try:
            if n == 1:
                pth = input('please enter the address of the file containing the strings: ')
                tree = dpda.createParseTree(dpda.dpda, pth)
                print('True') if tree else print('False')
            
            elif n == 2:
                pth = input('please enter the address of the file containing the strings: ')
                tree = dpda.createParseTree(dpda.dpda, pth)
                if tree: tree.PrintTree() 
                else: raise Exception('The string is not a member of the language')
                
            elif n == 3:
                pth = input('please enter the address of the file containing the strings: ')
                tree = dpda.createParsingTree(pth)
                if tree: tree.PrintTree() 
                else: raise Exception('The string is not a member of the language')
                
            elif n == 4:
                break
            
            elif n == 5:
                break
            
            else :
                exit(0)
                
        except Exception as ex:
            print(ex)
    
        