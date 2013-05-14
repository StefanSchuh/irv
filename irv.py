import sys

def bestremaining(remainingCandidates, vote):
    for c in vote:
        if c in remainingCandidates:
            return c
    return None

def redistributeVotes(remainingCandidates, votes):
    stacks= {}
    for vote in votes:
        bestCan=bestremaining(remainingCandidates,votes[vote])
        stacks.setdefault(bestCan,{})[vote]=votes[vote]
    return stacks

def askForTieBreak(tiedCandidates):
	print "Folgende Kandidaten sind gleich auf" 
	print tiedCandidates
	c = None
	while (c not in tiedCandidates):
		c = raw_input("Wer wir eleminiert?\n")
	return [c]


def breakTie(tiedCandidates):
    if len(tiedCandidates) > 1:
        return askForTieBreak(tiedCandidates)
    return [tiedCandidates[0]]

def printStack(stack):
    for candidate in stack:
        print str(candidate) + " hat "+ str(len(stack[candidate]))+" Stimmen auf seinem Stapel"
        for pseudoId in stack[candidate]:
            print str(pseudoId)+" : "+str(stack[candidate][pseudoId])


def findWinner(candidates,votes):
    while (1):
        stacks=redistributeVotes(candidates, votes)
        printStack(stacks)
        numberVotes = [len(stacks[x]) for x in candidates]
        if max(numberVotes) >= required:
            winner = filter(lambda x: len(stacks[x])>= required, candidates)[0]
            print "winner is ...." + winner
            return winner 
        print numberVotes
        minimum = min(numberVotes)
        tiedCandidates = filter(lambda x: len(stacks[x])==minimum , candidates)
        toBeRemoved = breakTie(tiedCandidates)
        print "Eliminiert: " + str(toBeRemoved)
        candidates = filter (lambda x: x not in toBeRemoved,candidates)

fileName = sys.argv[1] #"test-data/test.dat"
numberOfPositions = int(sys.argv[2]) # 2

f = open(fileName,'r')
votes = {}
i=1

for l in f:
    votes[i]=l.lower().split()
    i=i+1

f.close()

print len(votes)
print votes

print "Abgegebene Stimmen: " + str(len(votes))

required = len(votes)/2 + 1
print "noetige Stimmen: " + str(required)

acceptance = {}
for vote in votes.values():
    for c in vote:
        acceptance[c]=acceptance.setdefault(c,0)+1
        
print "Ergebnis der Akzeptanzwahl:"
candidates = sorted(acceptance.keys(),cmp=lambda x,y:acceptance[y]-acceptance[x])
for c in candidates:
	print str(c) + " " + str(acceptance[c])

remainingCandidates = filter(lambda x: acceptance[x] >= required, candidates)

print "Kandidaten mit mindestesten 50% der Stimmen: "+str(remainingCandidates)

numberOfPositions = min(numberOfPositions , len(remainingCandidates))

print "In dieser Wahl werden "+str(numberOfPositions)+" Personen gewaehlt."

for i in range(numberOfPositions):
    winner = findWinner(remainingCandidates, votes)
    remainingCandidates.remove(winner)
    









