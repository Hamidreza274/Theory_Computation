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
    print('please enter the on option')
    print('1.string Member of the Language?')
    print('2.ParseTree')
    print('3.change variable name')
    print('4.changeGrammer')
    print('5.Exit')
        
        
while True:
    path = input('please enter the address of the file containing the grammer:')
    dpda = DPDA(path)
    
    while True:
        n = intInput(1, 5, True)
        
        if n == 1:
            dpda.
        elif n == 2:
            pass
        elif n == 3:
            pass
        elif n == 4:
            break
        else :
            exit(0)
        