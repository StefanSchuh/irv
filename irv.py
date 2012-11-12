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
while not remainingCandidates and numberOfPositions > 0:
    stacks=redistributeVotes(remainingCandidates, votes)
    
print stacks

print candidates
print len(votes)
print votes







