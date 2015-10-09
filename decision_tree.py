#!/usr/bin/python

class Node:
    def __init__(self, description):
        self.description = description
        self.children = []
        self.parents = []
        decision = None  # this would be a function for directing movement to next child
        self.childpos = 0
        self.tag = False

    def add_child(self, other):
        self.children.append(other)
        other.parents.append(self)

    def add_children(self, others):
        for o in others:
            self.add_child(o)

    def cleanup(self):
        self.tag = False
        for c in self.children:
            c.cleanup()

    # does all the overhead processing for our traversal
    # spits out an array of parent->child relationships
    def inorderArray(self):
        s = ""
        s = self.inorder(s, None)
        self.cleanup()                  # resets the tags to all false
        s = filter(None,s.split("\n"))  # splits by line, removes empty 
        return s
    
    def inorder(self, s, lastp):
        if not self.tag:
            self.tag = True
            for c in self.children:
                s = c.inorder(s, self)
        if not lastp:
            s += "root"
        else:
            s += "%s -> %s \n" % (lastp.description, self.description)
        return s


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

root.add_child(A)
A.add_children([B, C, D, E])
D.add_children([E, C, F])
F.add_children([L, G, I])
C.add_children([L, K, J])

print "digraph G {"
for i in sorted(root.inorderArray()):
    if i:
        print i.strip(),";"
print "}"
