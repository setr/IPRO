#!/usr/bin/python

class Node:
    def __init__(self, description):
        self.description = description
        self.children = []
        self.parents = []
        decision = None  # this would be a function
        self.childpos = 0
        self.tag = False

    def __iter__(self):
        return self

    def next(self):
        if self.childpos < len(self.children):
            self.childpos += 1
            return self.children[self.childpos-1]
        else:
            self.childpos = 0
            raise StopIteration()

    def add_child(self, other):
        self.children.append(other)
        other.parents.append(self)

    def add_children(self, others):
        for o in others:
            self.add_child(o)
    
    def inorderArray(self):
        s = ""
        s = self.inorder(s, self.parents[0])
        s = filter(None,s.split("\n"))
        return s

    def inorder(self, s, lastp):
        if not self.tag:
            self.tag = True
            for c in self.children:
                s = c.inorder(s, self)
        s += "%s -> %s \n" % (lastp.description, self.description)
        return s

#root = Node(None,"root",None,None)

root = Node("root")
A = Node("Question1")
B = Node("Question2")
C = Node("Question3")
D = Node("Question4")
E = Node("Question5")
F = Node("Question6")
G = Node("Question7")
H = Node("Question8")
I = Node("Question9")
J = Node("Question10")
K = Node("Question11")
L = Node("Question12")

# root -> A
# A -> {B, C, D, E}
# D -> {E, C, F}
# F -> {L, M, N}
# C -> {X, Y, Z}

root.add_child(A)
A.add_children([B, C, D, E])
D.add_children([E, C, F])
F.add_children([L, G, I])
C.add_children([L, K, J])

print "digraph G {"
for i in sorted(A.inorderArray()):
    if i:
        print i.strip(),";"
print "}"
