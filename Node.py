from graphviz import Graph
from itertools import count

class Node:
    counter = 1
    def __init__(self, value):
        self.node_id = Node.counter
        self.value = value
        self.parent = None
        self.child = list()
        Node.counter += 1
    
    def preOrder(self, cur, lst):
        if cur is None : 
            return
        
        if cur is not None and len(cur.child) == 0 and cur.value != 'eps':
            cnt = cur.value.replace('\\', '')
            lst.append(cnt)
            
        for i in cur.child:
            self.preOrder(i, lst)
            
    
    def PrintTree(self):
        graph = Graph()
        self.pTree(graph, self)
        graph.render('ParsingTree', view=True)
        
        
    def pTree(self, graph: Graph, node, parent=None):
        
        graph.node( name=str(node.node_id), 
                    label=f"id:{node.node_id}\n{node.value}", 
                    shape='circle', 
                    width='1.2', 
                    height='1.2', 
                    style='filled',
                    color='blue' if len(node.child) != 0 else 'green', 
                    fontsize='10' if len(node.child) != 0 else '17', 
                    fixedsize='true'
                    )

        if parent != None:
            graph.edge(str(parent), str(node.node_id))
            
        for ch in node.child:
            self.pTree(graph, ch, node.node_id)
    
    
    def findNode(self, id):
        if self.node_id == id:
            return self
        
        for ch in self.child:
            res = ch.findNode(id)
            if res is not None:
                return res
            
        return None
        
        
    def changeValue(self, id, newValue):
        current = self.findNode(id)
        node = current
        
        while current.value != 'Block' and current.parent != None:
            current = current.parent
            
        self.change(current, newValue, node.value)
        
    
    def change(self, cur, newValue, oldValue):
        if cur.value == oldValue:
            cur.value = newValue
        
        for ch in cur.child:
            self.change(ch, newValue, oldValue)
            
    
    def createFile(self):
        lst = list()
        self.preOrder(self, lst)
        file = open('newFile.txt','w')
        file.write(' '.join(lst))
        
    # def __str__(self):
    #     return self.value 