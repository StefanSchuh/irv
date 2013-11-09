# -*- coding: utf-8 -*-
import argparse
import sys

def printAndProtokoll(msg):
    print msg
    out.write(msg+"\n")
    
def prettyListString(list):
    res = str(list[0])
    for e in list[1:]:
        res+=", "+str(e)
        
    return res
    
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
    printAndProtokoll("Folgende Kandidaten sind gleich auf: "+prettyListString(tiedCandidates)+".")
    c = None
    while (c not in tiedCandidates):
        c = raw_input("Wessen Stapel soll aufgelöst werden?\n")
    
    printAndProtokoll("Kandidat "+str(c)+" wurde ausgelost und scheidet somit aus.")
    return [c]


def breakTie(tiedCandidates):
    if len(tiedCandidates) > 1:
        return askForTieBreak(tiedCandidates)
    return [tiedCandidates[0]]

def printStack(stack):
    for candidate in sorted(stack):
        if candidate==None:
            printAndProtokoll( "Insgesamt sind "+ str(len(stack[candidate]))+" Stimmzettel aus der Wahl ausgeschieden.")
        else:
            printAndProtokoll( "Kandidat "+str(candidate) + " hat "+ str(len(stack[candidate]))+" Stimmen auf seinem Stapel.")
        #for pseudoId in stack[candidate]:
         #   print str(pseudoId)+" : "+str(stack[candidate][pseudoId])


def findWinner(candidates,votes):
    runde = 1
    while (1):
        stacks=redistributeVotes(candidates, votes)
        printAndProtokoll("Die Verteilung der Stimmen in der "+str(runde)+". Runde sieht wie folgt aus:")
        printStack(stacks)
        numberVotes = [len(stacks[x]) for x in candidates]
        if max(numberVotes) >= required:
            winner = filter(lambda x: len(stacks[x])>= required, candidates)[0]
            return winner 
        #print numberVotes
        minimum = min(numberVotes)
        tiedCandidates = filter(lambda x: len(stacks[x])==minimum , candidates)
        toBeRemoved = breakTie(tiedCandidates)
        printAndProtokoll( "Der Stapel des Kandidaten " + str(toBeRemoved[0])+u" wird aufgelöst.")
        candidates = filter (lambda x: x not in toBeRemoved,candidates)
        runde=runde+1



if not sys.argv[1:]: 
    sys.argv += ["test-data/LL_Top3_IRV#01", "3"] 


fileName = sys.argv[1] #"test-data/test.dat"
numberOfPositions = int(sys.argv[2]) # 2

if not sys.argv[3:]:
    sys.argv +=[fileName+".out"]


outName = sys.argv[3]

if not sys.argv[4:]:
    amtName= raw_input("Welches Amt soll besetzt werden?")
else:
    amtName = sys.argv[4]

f = open(fileName,'r')
out = open(outName,'w')
votes = {}
i=1

for l in f:
    votes[i]=l.lower().split()
    i=i+1

f.close()

#print len(votes)
#print votes


acceptance = {}
for vote in votes.values():
    for c in vote:
        acceptance[c]=acceptance.setdefault(c,0)+1
        
        

candidates = sorted(acceptance.keys())
printAndProtokoll("Es stehen "+ str(len(candidates))+" Kandidaten zur Wahl.")
for c in candidates:
    printAndProtokoll("Kandidat "+str(c)+": ")


printAndProtokoll("Es wurden insgesamt " + str(len(votes))+" Stimmen abgegeben.")

required = len(votes)/2 + 1

printAndProtokoll("Somit werden mindestens " + str(required)+u" Stimmen benötigt um gewählt zu werden.")



printAndProtokoll("Ergebnis der Akzeptanzwahl:")

for c in candidates:
	printAndProtokoll (str(c) + " " + str(acceptance[c]))

remainingCandidates = filter(lambda x: acceptance[x] >= required, candidates)

printAndProtokoll("Kandidaten die mehr als 50% der Stimmen haben: "+prettyListString(remainingCandidates))

numberOfPositions = min(numberOfPositions , len(remainingCandidates))

if numberOfPositions>1:
    printAndProtokoll("Somit werden in dieser Wahl "+str(numberOfPositions)+u" Personen gewählt.")


gewinner = []
for i in range(numberOfPositions):
    printAndProtokoll("\n==Wahl des "+str(i+1)+". "+amtName+"==\n")
    winner = findWinner(remainingCandidates, votes)
    printAndProtokoll("Kandidat " + winner+u" hat mehr als 50% der Stimmen auf seinem Stapel und gewinnt somit die Wahl zum "+str(i+1)+". "+amtName)
    gewinner.append(winner)
    remainingCandidates.remove(winner)

print "Folgende Kandidaten haben die Wahl gewonnen: "+ prettyListString(gewinner)
    
out.close()








