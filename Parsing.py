import re

class Parsing:
    def __init__(self, path):
        self.path = path
        self.startVar = None
        self.terminal = list()
        self.non_terminal = list()
        self.productions = dict()
        self.StringParser(path)
        
    def StringParser(self, path):
        file = open(path, "r").read()
        line = re.split('\n+', file)
        
        # startVar
        x = re.search(r"START\s=\s(.*)", line[0])
        self.startVar = x.group(1)
        
        # non_terminal
        x = re.search(r"^NON_TERMINALS\s+=\s+(.*)", line[1])
        self.non_terminal = x.group(1).split(' , ')
        
        # terminal
        x = re.search(r"^TERMINALS\s+=\s+(.*)", line[2])
        self.terminal = x.group(1).split(' , ')
        
        # Production
        for i in range(3, len(line)-1):
            x = re.split(r'\s+\|\s+|\s+->\s+', line[i])
            y = list()
            for j in x[1:]:
                y.append(j.split())
            self.productions[x[0]] = y
            
# A = Parsing('a.txt')
# print(A.terminal)
# print(A.productions)
# print('************')