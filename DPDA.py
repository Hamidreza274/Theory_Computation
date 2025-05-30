from Parsing import Parsing
from Node import Node
import re

class DPDA:
    def __init__(self, path):
        self.parse = Parsing(path)
        self.first = self.First()
        self.follow = self.Follow()
        self.table = self.CreateTable()
        self.dpda = self.createDPDA()
        
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
        while changed:
            changed = False
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
                
    
    def match(self, tk: str):
        for i in self.parse.terminalPattern:
            if re.match(i, tk):
                return self.parse.terminalPattern[i]
        return None
    
    
    def createNode(self, lst:list, var: list, num: list):
        nodeList = list()
        for i in lst:
            if i in self.parse.terminal:
                if i == self.parse.terminalPattern['[a-zA-Z_][a-zA-Z0-9_]*']:
                    nodeList.append(Node(var[0]))
                    var.remove(var[0])
                        
                elif i == self.parse.terminalPattern['-?\d+(\.\d+)?([eE][+-]?\d+)?']:
                    nodeList.append(Node(num[0]))
                    num.remove(num[0])
                    
                else:
                    for j in self.parse.terminalPattern:    
                        if self.parse.terminalPattern[j] == i:
                            nodeList.append(Node(j))
            else:
                nodeList.append(Node(i))
        return nodeList
    
    
    def createDPDA(self):
        dic = dict()
        dic[('q0', 'eps', '$')] = (f'{self.parse.startVar} $', 'q1')
        
        for variable in self.table:
            for token in self.table[variable]:
                dic[('q1', token, 'eps', variable)] = (self.table[variable][token], 'q1')
        
        for terminal in self.parse.terminal:
            dic[('q1', terminal, terminal)] = ('eps', 'q1')
            
        dic[('q1', 'eps', '$')] = ('$', 'q2')
        return dic
    
    
    # string prase with DPDA
    def createParseTree(self, dpda, path: str):
        string = open(path, 'r').read().split()
        var = [i for i in string if re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', i) and i not in self.parse.terminalPattern]
        num = [i for i in string if re.match(r'-?\d+(\.\d+)?([eE][+-]?\d+)?', i) and i not in self.parse.terminalPattern]
        print(var, num)
        string.append('$')
        counter = 0
        token = string[counter]
        state = 'q0'
        top = 0
        stack = [('$', None)]
        
        while token != '$' or stack != [('$', None)]:
            top = len(stack) - 1
            if (state, self.match(token), stack[top][0]) in dpda:
                update = dpda[(state, self.match(token), stack[top][0])]
                state = update[1]
                cur = stack.pop()
                counter += 1
                token = string[counter]
                if update[0] == 'eps' and cur[0] in self.parse.terminal: continue
                nodes = self.createNode(update[0].split(), var, num)
                cur[1].child = nodes
                if update[0] == 'eps': continue
                stack.extend(list(reversed(list(zip(update[0].split(), nodes)))))
                 
            elif (state, self.match(token), 'eps', stack[top][0]) in dpda or (state, '$', 'eps', stack[top][0]) in dpda:
                lookahead = self.match(token) if self.match(token) is not None else '$'
                update = dpda[(state, lookahead, 'eps', stack[top][0])]
                state = update[1]
                cur = stack.pop()
                if update[0] == 'eps' and cur[0] in self.parse.terminal: continue
                nodes = self.createNode(update[0].split(), var, num)
                cur[1].child = nodes
                if update[0] == 'eps': continue
                stack.extend(list(reversed(list(zip(update[0].split(), nodes)))))
                
            # elif (state, self.match(token), 'eps') in dpda:
            #     update = dpda[(state, self.match(token), 'eps')]
            #     state = update[1]
            #     nodes = self.createNode(update[0].split())
            #     cur[1].child = nodes
            #     if update[0] != 'eps': stack.extend(list(reversed(list(zip(update[0].split(), nodes)))))
            #     counter += 1
            #     token = string[counter]
                
            # elif (state, 'eps', 'eps') in dpda:
            #     update = dpda[(state, 'eps', 'eps')]
            #     state = update[1]
            #     nodes = self.createNode(update[0].split())
            #     cur[1].child = nodes
            #     if update[0] != 'eps': stack.extend(list(reversed(list(zip(update[0].split(), nodes)))))
            
            elif ('q0', 'eps', '$') in dpda:
                tree = Node(self.parse.startVar)
                stack.append((self.parse.startVar, tree))
                state = 'q1'
                
            else:
                return False
        return tree
    
    
    # string prase with stack & parseTable & lookahead
    def createParsingTree(self, path: str):
        stack = []
        string = open(path, 'r').read().split()
        stack.append(('$', None))
        tree = Node(self.parse.startVar)
        stack.append((self.parse.startVar, tree))
        pointer = 0
        top = 1
        counter = 0
        lookahead = self.match(string[counter])
        
        while len(stack) != 0:
            if stack[top][0] == '$' and lookahead == '$':
                stack.pop(top)
                top -= 1
                
            elif lookahead == stack[top][0]:
                counter += 1
                stack.pop(top)
                top -= 1
                lookahead = '$' if len(string) == counter else self.match(string[counter])
                
            
            elif self.table[stack[top][0]].get(lookahead, None) is not None:
                lst = self.table[stack[top][0]][lookahead].split()
                lst2 = []
                cur = stack.pop(top)[1]
                if lst == ['eps']:
                    cur.child.append(Node('eps'))
                    top -= 1
                    continue

                for i in lst:
                    node = Node(i) if i in self.parse.non_terminal else Node(string[pointer])
                    if i in self.parse.terminal:
                        pointer += 1 
                    cur.child.append(node)
                    lst2.append((i, node))
                    
                lst2.reverse()
                stack.extend(lst2)
                top += len(lst2) - 1
                
            else:
                return False
        return tree