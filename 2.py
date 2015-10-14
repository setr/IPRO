#!/usr/bin/python
import sys
import pprint


variableInFile = "vals.txt"
decisionTreeFile = "input.txt"

state = {}

# reads the two files
def read():
    class item:
        def __init__(self, cat, desc, funcs):
            self.cat = cat  # category name; ie node name
            self.desc = desc
            self.funcs = funcs
        def getNext(self, state):
            if self.funcs:
                for func in self.funcs:
                    if func.act(state):
                        return func.out
                raise Exception("No valid move from " + self.cat + " but not a leaf")
            else:
                return None

    # if [condition] go [target]
    # basically just stores that shit
    class conj:
        def __init__(self, func1, func2, join):
            self.func1 = func1
            self.func2 = func2
            self.out = None
            join = join.strip()
            if join == "and":
                self.act = self.andj
            elif join == "or":
                self.act = self.orj
            elif join == "None":   # second function is empty
                self.act = self.func1.act
            else:
                raise Exception("invalid join")
        def andj(self, state):
            return (self.func1.act(state) and self.func2.act(state))
        def orj(self, state):
            return (self.func1.act(state) or self.func2.act(state))
        def printa(self):
            if self.func1:
                print self.func1.printfunc()
            if self.func2:
                print self.func2.printfunc()
            print "GOTO", self.out

    class func:
        def __init__(self, name, act, val):
            actdict = {
                    "eq": self.eq,
                    "gt": self.gt,
                    "gteq": self.gteq,
                    "lt": self.lt,
                    "lteq": self.lteq,
                    "else": self.rest}
            self.name = name
            self.val = val
            self.act = actdict[act]

        def printfunc(self):
            return self.name, self.val, self.act 
        def eq(self,state):
            return state[self.name] == self.val
        def gt(self,state):
            return state[self.name] > self.val 
        def gteq(self,state):
            return state[self.name] >= self.val 
        def lt(self,state):
            return state[self.name] < self.val 
        def lteq(self,state):
            return state[self.name] <= self.val 
        def rest(self,state):  # else .. the rest
            return True

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
        def getCondition(words, i):
            if i+3 <= len(words)-2:
                name = words[i]
                action = act[words[i+1]]
                val = words[i+2]
                return func(name, action, val)
            else:
                return None

        lastconj = None
        words = line.split(" ")
        words = [word.strip() for word in words]
        act = { "=":"eq",
                ">": "gt",
                ">=": "gteq",
                "<": "lt",
                "<=": "lteq"}
        action = ""
        if words[0] == "if":
            first = True
            lastconj = None
            laststmnt = None
            for i in xrange(1, len(words)-2, 4):
                newfunc = getCondition(words, i)
                if first:
                    lastconj = conj(newfunc, None, "None")
                    lastconj.out = words[len(words)-1]
                    first = False
                else:
                    if laststmnt == "or" or laststmnt == "and":
                        lastconj = conj(lastconj, newfunc, laststmnt)
                        lastconj.out = words[len(words)-1]
                    #elif laststmnt == "go":
                    #    lastconj.out = words[i+4]
                    else:
                        raise Exception(line, + "can't be parsed as conditionals")
                laststmnt = words[i+3]
        elif words[0] == "else":
            if words[1]:
                name = None
                action = "else"
                val = None
                func1 = func(name, action, val)
                lastconj = conj(func1, None, "None")
                lastconj.out = words[1]
        else:
            raise Exception(line + " can't be parsed as a function")
        return lastconj

    def readItems(f):
        items = []
        for line in f:
            line = line.strip()
            if line and line[0] is not "#":  # found a new node
                cat = line
                desc = next(f).strip()
                funcs = list()
                while True:  # now we start reading the conditions 
                    line = next(f).strip()
                    if line:  # stop if the line is empty
                        if line[0] is not "#":  # skip if the line is a comment
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
    
# just pretty-prints the state values
def pprintState():
    print
    print "INPUT VALUES READ AS:"
    print "Attribute".ljust(15), "Value".ljust(15)
    for k,v in state.iteritems():
        print "", k.ljust(16), v.ljust(15)
    print 

if __name__=="__main__":
    items = read()
    pprintState()
    leaf = getLeaf(items[0],items)
    print "DECISION NODE REACHED:", leaf.cat
    print "RECOMMENDATION:", leaf.desc
    print
