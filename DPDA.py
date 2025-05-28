from Parsing import Parsing
from Node import Node

class DPDA:
    def __init__(self, path):
        self.parse = Parsing(path)
        self.first = self.First()
        self.follow = self.Follow()
        self.table = self.CreateTable()
        
    def First(self):
        dic = dict()
        for variable in self.parse.productions:
            dic[variable] = dict()
            for production in self.parse.productions[variable]:
                dic[variable][' '.join(production)] = self.firstf(production)
        return dic

                
    def firstf(self, production: list, k=0):
        if production[k] == 'eps':
            return ['eps']
        
        if production[k] in self.parse.terminal:
            return [production[k]]
        
        elif production[k] in self.parse.non_terminal:
            lst = list()
            for x in range(k, len(production)):
                for pro in self.parse.productions[production[x]]:
                    lst.extend(self.firstf(pro))
                    
                if 'eps' not in lst:
                    break
                lst.remove('eps')
            return lst
        
    def lenT(self, dic: dict):
        s = 0
        for variable in dic:
            s += len(dic[variable])
        return s
    
    def Follow(self):
        dic = {nt: [] for nt in self.parse.non_terminal}
        dic[self.parse.startVar].append('$')
        
        changed = True
        m = 0
        while m != 10:
            changed = False
            m += 1
            for variable in self.parse.productions:
                for production in self.parse.productions[variable]:
                    for entity in range(len(production)):
                        if production[entity] in self.parse.terminal:
                            continue

                        target = production[entity] if production[entity] != 'eps' else variable
                        before = self.lenT(dic)
                        
                        if production[entity] == 'eps' or entity == len(production) - 1:
                            dic[target].extend([x for x in dic[variable] if x not in dic[target]])
                            
                            
                        elif production[entity + 1] in self.parse.terminal:
                            if production[entity + 1] not in dic[target]:
                                dic[target].append(production[entity + 1])

                        else:
                            lst = list()
                            for z in range(entity + 1, len(production)):
                                for x in self.first[production[z]].values():
                                    for y in x:
                                        lst.append(y)
                                if 'eps' not in lst:
                                        break
                                if 'eps' in lst and z == len(production) - 1:
                                    lst.extend(dic[variable])
                                lst.remove('eps')
                                
                            dic[target].extend(x for x in lst if x != 'eps' and x not in dic[target])
                          
                        if self.lenT(dic) > before:
                                    changed = True
        return dic
            
    
    def CreateTable(self):
        dic = dict()
        for var in self.parse.non_terminal:
            dic[var] = dict()
             
        for variable in self.first:
            for production in self.first[variable]:
                for first in self.first[variable][production]:
                    if first == 'eps':
                        for follow in self.follow[variable]:
                            dic[variable][follow] = production
                    else:
                        dic[variable][first] = production
        return dic
                
                
    def createParsingTree(self, string: str):
        stack = []
        string = string.split()
        stack.append(('$', None))
        tree = Node(self.parse.startVar)
        stack.append((self.parse.startVar, tree))
        top = 1
        counter = 0
        lookahead = string[counter]
        
        while len(stack) != 0:
            print([x for x, y in stack])
            if stack[top][0] == '$' and lookahead == '$':
                stack.pop(top)
                top -= 1
                
            elif lookahead == stack[top][0]:
                counter += 1
                stack.pop(top)
                top -= 1
                lookahead = '$' if len(string) == counter else string[counter]
                
            
            elif self.table[stack[top][0]].get(lookahead, None) is not None:
                lst = self.table[stack[top][0]][lookahead].split()
                lst2 = []
                cur = stack.pop(top)[1]
                if lst == ['eps']:
                    cur.child.append(Node('eps'))
                    top -= 1
                    continue

                for i in lst:
                    node = Node(i)
                    cur.child.append(node)
                    lst2.append((i, node))
                    
                lst2.reverse()
                stack.extend(lst2)
                top += len(lst2) - 1
                
            else:
                return False
        return tree
        
    
a = DPDA('a.txt')
# print(a.parse.productions)
# print("*******")
# print(a.first)
# print('**********')
# print(a.follow)
# print('//////////////////')
# print(a.table)
tree = a.createParsingTree("( IDENTIFIER RIGHT_PAR LEFT_PAR IDENTIFIER RIGHT_PAR")
tree.PrintTree()
