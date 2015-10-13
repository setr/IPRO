#!/usr/bin/python
import sys

state = {}
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


def read():
    class item:
        def __init__(self, cat, desc, funcs):
            self.cat = cat
            self.desc = desc
            self.funcs = funcs
        def getNext(self, state):
            if self.funcs:
                for func in self.funcs:
                    nextName = func.act(state)
                    if nextName:
                        return nextName
                raise Exception("No valid move from " + self.cat + " but not a leaf")
            else:
                return None

    class func:
        def __init__(self, name, act, val, out):
            self.name = name
            self.val = val
            self.out = out
            if act == "eq":
                self.act = self.eq
            elif act == "gt":
                self.act = self.gt
            elif act == "gteq":
                self.act = self.gteq
            elif act == "lt":
                self.act = self.lt
            elif act == "lteq":
                self.act = self.lteq
            elif act == "else":
                self.act = self.rest
        def eq(self,state):
            return self.out if state[self.name] == self.val else None
        def gt(self,state):
            return self.out if state[self.name] > self.val else None
        def gteq(self,state):
            return self.out if state[self.name] >= self.val else None
        def lt(self,state):
            return self.out if state[self.name] < self.val else None
        def lteq(self,state):
            return self.out if state[self.name] <= self.val else None
        def rest(self,state):  # else .. the rest
            return self.out

    def readValues(f):
        states = {}
        for line in f:
            line = line.strip()
            words = line.split(":")
            words = [word.strip() for word in words]
            states[words[0]] = word[1]
        return states

    def readFunc(line):
        words = line.split(" ")
        words = [word.strip() for word in words]
        act = { "=":"eq",
                ">": "gt",
                ">=": "gteq",
                "<": "lt",
                "<=": "lteq"}
        action = ""
        if words[0] == "if":
            if words[2]:
                name = words[1]
                action = act[words[2]]
                val = words[3]
                target = words[5]
        elif words[0] == "else":
            if words[1]:
                name = None
                action = "else"
                val = None
                target = words[1]
        else:
            raise Exception(line + " can't be parsed as a function")
        func2 = func(name, action, val, target)
        return func2

    def readItems(f):
        items = []
        for line in f:
            line.strip()
            if line:
                cat = line
                desc = next(f).strip()
                funcs = list()
                while True:
                    line = next(f).strip()
                    if line:
                        func = readFunc(line)
                        funcs.append(func)
                    else:
                        break
                newitem = item(cat, desc, funcs)
                items.append(newitem)
        return items

    global state
    with file("vals.txt", "r") as f:
        state = readValues(f)
    with file("input.txt", "r") as f:
        items = readItems(f)

    print state
    for item in items:
        a = item.getNext(state)
        if a:
            print a
        else:
            print item.cat, "LEAF"
        #print item.cat, item.desc

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

read()

# because lazy; if any args, print for graphing
#  if sys.argv[1:]:
#      print graphviz_out()
#  else:
#      print find_level(None).description
