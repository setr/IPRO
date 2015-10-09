#!/usr/bin/python
import sys

# this is the function determining movement
# for testing, all are just going to the highest question number
# in practice, when instantiating our nodes, we'd add how it determines
    # movement as well. (go to child 2 if methane > 60 ...)
# must always have variables and children for args, but body can be w/e.
def moveTo(variables, children):
    hival = int(children[0].description[-2:])
    hic = children[0]
    for c in children:
        newval = int(c.description[-2:])
        if hival < newval:
            hival = newval
            hic = c
    return hic

class Node:
    def __init__(self, description, decision=moveTo):
        self.description = description
        self.children = []
        self.parents = []
        self.decision = decision # this would be a function for directing movement to next child
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

    # simply runs through the tree using the node's given path determination function
    def find_level(self, variables):
        if self.children:
            nextNode = self.decision(variables, self.children)
            return nextNode.find_level(variables)
        else:
            return self

    # does all the overhead processing for our traversal
    # used by graphviz_out
    def inorderArray(self):
        s = ""
        s = self.inorder(s, None).split("\n")
        self.cleanup()                  # resets the tags to all false
        s = filter(None,s)  # splits by line, removes empty lines
        return s

    # only intended for use by inorderArray
    def inorder(self, s, lastp):
        if not self.tag:
            self.tag = True
            for c in self.children:
                s = c.inorder(s, self)
        if lastp:  # skips printing a parent for root, since it has none..
            # %-10s just adds left-side padding to gaurantee min. 10 chars for that string
            s += "%-10s -> %s \n" % (lastp.description, self.description)
        return s

# spits out an array of parent->child relationships for graphviz
def graphviz_out():
    s = "digraph G {\n"
    for i in sorted(root.inorderArray()):
        s += "  " + i.strip() + ";\n"
    s += "}"
    return s

# we only ever start from root..
def find_level(variables):
    return root.find_level(variables)


root = Node("root")
A = Node("Question01")
B = Node("Question02")
C = Node("Question03")
D = Node("Question04")
E = Node("Question05")
F = Node("Question06")
G = Node("Question07")
H = Node("Question08")
I = Node("Question09")
J = Node("Question10")
K = Node("Question11")
L = Node("Question12")

root.add_child(A)
A.add_children([B, C, D, E])
D.add_children([E, C, F])
F.add_children([L, G, I])
C.add_children([L, K, J])

# because lazy; if any args, print for graphing
if sys.argv[1:]:
    print graphviz_out()
else:
    print find_level(None).description
