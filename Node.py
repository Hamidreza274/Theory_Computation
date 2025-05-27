class Node:
    def __init__(self, value):
        self.value = value
        self.child = list()
        self.parent = None
    
    def preOrder(self, cur):
        if cur is not None:
            print(cur.value)
            
            for i in cur.child:
                self.preOrder(i)
    
    def __str__(self):
        return self.value