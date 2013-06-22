# -*- coding: utf-8 -*-
import sys,argparse

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
	print "Folgende Kandidaten sind gleich auf: " 
	print tiedCandidates
	c = None
	while (c not in tiedCandidates):
		c = raw_input("Wessen Stapel soll aufgelöst werden?\n")
	return [c]


def breakTie(tiedCandidates):
    if len(tiedCandidates) > 1:
        return askForTieBreak(tiedCandidates)
    return [tiedCandidates[0]]

def printStack(stack):
    for candidate in sorted(stack):
        if candidate==None:
            print "Insgesamt sind "+ str(len(stack[candidate]))+" Stimmzettel auf keinem Stapel."
        else:
            print "Kandidat "+str(candidate) + " hat "+ str(len(stack[candidate]))+" Stimmen auf seinem Stapel."
        #for pseudoId in stack[candidate]:
         #   print str(pseudoId)+" : "+str(stack[candidate][pseudoId])


def findWinner(candidates,votes):
    runde = 1
    while (1):
        stacks=redistributeVotes(candidates, votes)
        print "Die Verteilung der Stimmen in der "+str(runde)+". Runde:"
        printStack(stacks)
        numberVotes = [len(stacks[x]) for x in candidates]
        if max(numberVotes) >= required:
            winner = filter(lambda x: len(stacks[x])>= required, candidates)[0]
            return winner 
        #print numberVotes
        minimum = min(numberVotes)
        tiedCandidates = filter(lambda x: len(stacks[x])==minimum , candidates)
        toBeRemoved = breakTie(tiedCandidates)
        print "Der Stapel des Kandidaten " + str(toBeRemoved[0])+u" wird aufgelöst."
        candidates = filter (lambda x: x not in toBeRemoved,candidates)
        runde=runde+1

if not sys.argv[1:]: 
    sys.argv += ["test-data/LL_Top3_IRV#01", "3"] 


fileName = sys.argv[1] #"test-data/test.dat"
numberOfPositions = int(sys.argv[2]) # 2

f = open(fileName,'r')
votes = {}
i=1

for l in f:
    votes[i]=l.lower().split()
    i=i+1

f.close()

#print len(votes)
#print votes

print "Es wurden insgesammt " + str(len(votes))+" Stimmen abgegeben."

required = len(votes)/2 + 1
print "Es werden somit mindestens " + str(required)+u" Stimmen benötigt um gewählt zu werden."

acceptance = {}
for vote in votes.values():
    for c in vote:
        acceptance[c]=acceptance.setdefault(c,0)+1
        
print "Ergebnis der Akzeptanzwahl:"
candidates = sorted(acceptance.keys())
for c in candidates:
	print str(c) + " " + str(acceptance[c])

remainingCandidates = filter(lambda x: acceptance[x] >= required, candidates)

print "Kandidaten die mehr als 50% der Stimmen haben: "+str(remainingCandidates)

numberOfPositions = min(numberOfPositions , len(remainingCandidates))

print "Somit werden in dieser Wahl "+str(numberOfPositions)+u" Personen gewählt."


gewinner = []
for i in range(numberOfPositions):
    winner = findWinner(remainingCandidates, votes)
    print "Kandidat " + winner+u" hat mehr als 50% der Stimmen auf seinem Stapel und gewinnt somit die Wahl für den "+str(i+1)+". Posten."
    gewinner.append(winner)
    remainingCandidates.remove(winner)

print "Folgende Kandidaten haben die Wahl gewonnen: "+ str(gewinner)
    









