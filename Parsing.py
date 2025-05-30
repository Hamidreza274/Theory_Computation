import re

class Parsing:
    def __init__(self, path):
        self.path = path
        self.startVar = None
        self.terminal = list()
        self.non_terminal = list()
        self.productions = dict()
        self.terminalPattern = dict()
        self.StringParser(path)
        
    def StringParser(self, path):
        file = open(path, "r").read()
        lines = re.split('\n+', file)
        lines = [i for i in lines if not re.match(r'^\s*#', i)]
        
        # startVar
        x = re.search(r"START\s=\s(.*)", lines[0])
        self.startVar = x.group(1)
        
        # non_terminal
        x = re.search(r"^NON_TERMINALS\s+=\s+(.*)", lines[1])
        self.non_terminal = x.group(1).split(' , ')
        
        # terminal
        x = re.search(r"^TERMINALS\s+=\s+(.*)", lines[2])
        self.terminal = x.group(1).split(' , ')
        
        # Production
        for i in range(3, len(lines)-1):
            x = re.split(r'\s+\|\s+|\s+->\s+', lines[i])
            
            if x[0] in self.terminal:
                self.terminalPattern[x[1]] = x[0]
                continue
            
            y = list()
            for j in x[1:]:
                y.append(j.split())
            self.productions[x[0]] = y