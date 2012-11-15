import sys

def bestremaining(remainingCandidates, vote):
    for c in vote:
        if c in remainingCandidates:
            return c
    return None

def redistributeVotes(remainingCandidates, votes):
    stacks= {}
    for vote in votes:
        bestCan=bestremaining(remainingCandidates,vote)
        stacks.setdefault(bestCan,list()).append(vote)
    return stacks

# for now remove all 
def breakTie(tiedCandidates):
    if len(tiedCandidates) > 1:
        print "shit!"
    return tiedCandidates

fileName = sys.argv[1]
numberOfPositions = int(sys.argv[2])

f = open(fileName,'r')
votes = []

for l in f:
    votes.append(l.lower().split())

f.close()

required= len(votes)/2 + 1

acceptance = {}
for vote in votes:
    for c in vote:
        acceptance[c]=acceptance.setdefault(c,0)+1
        
print acceptance

candidates = sorted(acceptance.keys())
remainingCandidates = filter(lambda x: acceptance[x] >= required, candidates)

print remainingCandidates

numberOfPositions = min(numberOfPositions , len(remainingCandidates))

while numberOfPositions > 0:
    stacks=redistributeVotes(remainingCandidates, votes)
    print stacks
    numberVotes = [len(stacks[x]) for x in remainingCandidates]
    if max(numberVotes) >= required:
        winner = filter(lambda x: len(stacks[x])>= required, remainingCandidates)[0]
        print "winner is ...." + winner
        remainingCandidates.remove(winner)
        numberOfPositions = numberOfPositions - 1
        continue
        
    
    print numberVotes
    minimum = min(numberVotes)
    tiedCandidates = filter(lambda x: len(stacks[x])==min , remainingCandidates)
    toBeRemoved = breakTie(tiedCandidates)
    remainingCandidates = filter (lambda x: x not in toBeRemoved,remainingCandidates)
    

print candidates
print len(votes)
print votes







