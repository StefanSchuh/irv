import sys

def bestremaining(remainingCandidates, vote):
    for c in vote:
        if c in remainingCandidates:
            return c
    return None

def createstacks(remainingCandidates, votes):
    stacks= dict.fromkeys(remainingCandidates,[])
    bestcandidates = [bestremaining(remainingCandidates,vote) for vote in votes]
    print bestcandidates    
    return stacks


fileName = sys.argv[1]
numberOfPositions = int(sys.argv[2])

f = open(fileName,'r')
votes = []

for l in f:
    votes.append(l.lower().split())

f.close()

acceptance = {}
for vote in votes:
    for c in vote:
        acceptance[c]=acceptance.setdefault(c,0)+1

candidates = sorted(acceptance.keys(), key=lambda x: acceptance[x])


createstacks(candidates, votes)

print candidates
print len(votes)
print votes
print acceptance






