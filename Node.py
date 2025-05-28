from graphviz import Graph
from itertools import count

class Node:
    def __init__(self, value):
        self.value = value
        self.child = list()
    
    def preOrder(self, cur):
        if cur is not None:
            print(cur.value)
            
            for i in cur.child:
                self.preOrder(i)
    
    def PrintTree(self):
        graph = Graph()
        counter = count(1)
        self.pTree(graph, self, counter)
        graph.render('ParsingTree', format='png')
        
        
    def pTree(self, graph: Graph, node, counter, parent=None):
        node_id = str(next(counter))
        
        graph.node( name=node_id, 
                    label=node.value, 
                    shape='circle', 
                    width='0.75', 
                    height='0.75', 
                    style='filled',
                    color='blue' if len(node.child) != 0 else 'green', 
                    fontsize='8', 
                    fixedsize='true'
                    )

        if parent != None:
            graph.edge(parent, node_id)
            
        for ch in node.child:
            self.pTree(graph, ch, counter, node_id)
    
    
    def __str__(self):
        return self.value