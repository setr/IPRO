#!/usr/bin/python
import argparse
# this program compares the inputted condition values against the metrics for warning levels.



# defaults; modified by argument flags
filename = "vault_condition.txt" 
matcher = None  # meet the min. requirements of one or all to match level?

class WarningLevel:
    levelnum = 0
    outputstring = ""
    baseconditions = []

    def __init__(self, level, output, condition):
        self.levelnum = level
        self.outputstring = output
        self.baseconditions = condition
    
    # less than; for built-in sorting by level number.
    def __lt__(self, other):
        return self.levelnum < other.levelnum

    # compares input against conditions necessary for warning level
    # matcher is either the builtin any or all; 
    # any being true if any condition is greater than the minimums for this level
    # all being true if all conditions are greater than the minimums for this level
    def checkIfMeets(self, condition):
        return matcher(self.baseconditions[i] <= cond for i, cond in enumerate(condition))

def FixConditionsString(conditions):
    conditions = conditions.split(",")
    # now we need to make it numbers, with error handling..
    if all(cond.isdigit() for cond in conditions):
        conditions = [int(cond) for cond in conditions]
        return conditions
    else:
        error = conditions + "is not valid; needs to be comma deliminated list of numbers."
        raise ValueError(error)

def getWarningLevels():
    # I don't care how many conditions you want to check against
    # But I do care that they're consistent in number.
    oldlen = 0  
    
    levels = []
    with open(filename, "r") as f:
        for index, line in enumerate(f):
            line = line.strip()
            if line and not line[0] == "#" and line.isdigit():  # ignoring empty lines and comment lines, first line for a set should just be a digit
                # get this line, and the next 3..
                level = int(line)
                comment = next(f).strip()
                conditions = next(f).strip()  # comma-deliminated list of numbers
                conditions = FixConditionsString(conditions) # parses into an array of numbers; if it fails, throws an error

                # make sure condition numbers are consistent...
                if oldlen == 0:
                    oldlen = len(conditions)
                elif oldlen != len(conditions):
                    error = "Inconsistent condition number, found %d where previous was %d \nOn line: %d" % (len(conditions), oldlen, index)
                    raise IndexError(error)
                newlevel = WarningLevel(level, comment, conditions)
                levels.append(newlevel)
    return levels, oldlen

def printinfo(found, orderedLevels, curcond):
    print found.outputstring
    print "Min requirement: ", found.baseconditions
    print "Our conditions:  ", curcond
    if found.levelnum < len(list(orderedLevels)):
        print "Next level mins':", list(reversed(orderedLevels))[found.levelnum].baseconditions
    else:
        print "MAXED"

def main(curcond):
    levels, condlen = getWarningLevels()  # reads the txt file for warning levels, returns the level array and length of conditions in txt
    if len(curcond) != condlen: 
        error = ("Number of variables given for the condition of the vault does not match "
            "the number of variables being used by the decision tree. You gave %d items, the decision "
            "tree uses %d" % (len(curcond), condlen))
        raise IndexError(error)

    orderedLevels = sorted(levels, reverse=True)  # orders it, from highest to lowest.
    # checks each warning level's conditions against our current conditions
    # first match is all we need, since its in order of worst to best.
    found = next(level for level in orderedLevels if level.checkIfMeets(curcond))
    printinfo(found, orderedLevels, curcond)

# handles all our flags and such. Passes just the conditions array back up for main to use.
def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('conditions', metavar="C", type=int, nargs='+',
            help="Condition of the Vault being tested; a sequence of values corresponding to conditions")
    parser.add_argument('--infile', action="store", type=str, 
            help="specify input file; default = a.txt")
    parser.add_argument('--anymatch', action="store_const", const=any, default=all,
            help="meet any min. value to declare vault condition; default is meet all minimums")
    args = parser.parse_args()
    
    global matcher 
    matcher = args.anymatch
    if args.ifile:
        filename = infile  # sets the global'd variable for file input
    return args.conditions

# EVERYTHING BEGINS HERE
if __name__ == '__main__':
    conditions = parse()
    main(conditions)  
