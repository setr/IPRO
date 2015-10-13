#!/usr/bin/python
import sys

variableInFile = "vals.txt"
decisionTreeFile = "input.txt"

state = {}

# reads the two files
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

    # if [condition] go [target]
    # basically just stores that shit
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
            if line and line[0] is not "#":
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

    def getNextNotComment(f):
        while True:
            line = next(f)
            line = line.strip()
            if line and line[0] is not "#":
                return line
            
    def readItems(f):
        items = []
        for line in f:
            line = line.strip()
            if line and line[0] is not "#":
                cat = line
                # desc = getNextNotComment(f)
                # print cat, desc
                desc = next(f).strip()
                funcs = list()
                while True:
                    #line = getNextNotComment(f)
                    line = next(f).strip()
                    if line and line[0] is not "#":
                        func = readFunc(line)
                        funcs.append(func)
                    else:
                        break
                newitem = item(cat, desc, funcs)
                items.append(newitem)
        return items

    global state
    with file(variableInFile, "r") as f:
        state = readValues(f)
    with file(decisionTreeFile, "r") as f:
        items = readItems(f)
    return items


def findNextNode(nextCat, items):
    for item in items:
        if item.cat.strip() == nextCat:
            return item
    raise Exception("Next Node Doesn't Exist: " + nextCat)

def getLeaf(item, items):
    nextCat = item.getNext(state)
    if nextCat:
        nextItem = findNextNode(nextCat, items)
        return getLeaf(nextItem, items)
    if not nextCat:
        return item
    
if __name__=="__main__":
    items = read()
    leaf = getLeaf(items[0],items)
    print leaf.cat, leaf.desc
