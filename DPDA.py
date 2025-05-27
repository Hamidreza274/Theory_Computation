from Parsing import Parsing

class DPDA:
    def __init__(self, path):
        self.parse = Parsing(path)
        self.first = self.First()
        self.follow = self.Follow()
        # self.table = self.CreateTable(self.first, self.follow)
        
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
        
        
    def Follow(self):
        dic = {nt: [] for nt in self.parse.non_terminal}
        dic[self.parse.startVar].append('$')

        changed = True
        while changed:
            changed = False
            for variable in self.parse.productions:
                for production in self.parse.productions[variable]:
                    for entity in range(len(production)):
                        if production[entity] in self.parse.terminal or production[entity] == 'eps':
                            continue

                        target = production[entity]
                        before = len(dic[target])

                        if entity == len(production) - 1:
                            dic[target].extend([x for x in dic[variable] if x not in dic[target]])
                            
                            
                        elif production[entity + 1] in self.parse.terminal:
                            if production[entity + 1] not in dic[target]:
                                dic[target].append(production[entity + 1])

                        else:
                            dic[target].extend(x for x in list(self.first[production[entity + 1]].values()) if x != 'eps' and x not in dic[target])
                            
                        if len(dic[target]) > before:
                                    changed = True
        return dic
            
    
    # def CreateTable(self):
    #     for variable in self.first:
    #         for f in 
    
    
a = DPDA('a.txt')
print(a.parse.productions)
print("*******")
print(a.first)
print('**********')
print(a.follow)