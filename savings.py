import json
import util
import operator
from audioop import reverse
import new
from itertools import repeat

customerServed = dict()
distanceDict = dict()
vehicleCap = 100
def func(customerPosDemand, depot):
    # refer link - http://ieeexplore.ieee.org/document/7784340/?reload=true
    #Step 1
    savings = dict()
    customerPositions =  customerPosDemand.keys()
    pointsLen = len(customerPositions)
    for i in range(pointsLen):
        for j in range(i+1,pointsLen):
            distanceDict[(customerPositions[i], customerPositions[j])] = util.euclideanDistance(customerPositions[i], customerPositions[j])

    #Step 2
    for i in range(pointsLen):
        for j in range(i+1,pointsLen):
            savings[(customerPositions[i], customerPositions[j])] = computeSaving(depot,customerPositions[i], customerPositions[j])
    savings = sorted(savings.items(),key=operator.itemgetter(1),reverse=True)
    # print(savings)
    l = len(savings)
    cust_pairs = list()
    for i in range(l):
        cust_pairs.append(savings[i][0])

    #initially none of the customers have been isServed
    for c in customerPositions:
        customerServed[c] = False

    #Step 3                  
    routes = dict()
    l = len(cust_pairs)
    i = 0
    idx = -1
    truck = [0,0,0,0,0]
    # print(cust_pairs)

    #choosing the maximum savings customers who are unserved
    for c in cust_pairs:
        if (isServed(c[0]) == False and isServed(c[1]) == False):
            hasBeenServed(c[0])
            hasBeenServed(c[1])
            idx += 1
            routes[idx] = ([c[0],c[1]]) 
            break
            
    #finding a cust that is either at the start or end of previous route
    for c in cust_pairs:
        res = inPrevious(c[0], routes[idx])
        if res == 0 and capacityValid(routes[idx], c[1], customerPosDemand) and (isServed(c[1]) == False):
            hasBeenServed(c[1])
            routes[idx].append(c[1]) 
        elif res == 1 and capacityValid(routes[idx], c[1], customerPosDemand) and (isServed(c[1]) == False):
            hasBeenServed(c[1])
            routes[idx].insert(0,c[1])
        else:
            res = inPrevious(c[1], routes[idx])
            if res == 0 and capacityValid(routes[idx], c[0], customerPosDemand) and (isServed(c[0]) == False):
                hasBeenServed(c[0])
                routes[idx].append(c[0]) 
            elif res == 1 and capacityValid(routes[idx], c[0], customerPosDemand) and (isServed(c[0]) == False):
                hasBeenServed(c[0])
                routes[idx].insert(0,c[0])

    # printing each truck load
    for r in routes.values():
        cap = 0
        for points in r:
            cap += customerPosDemand[points]
        # print(cap)


    #adding depot at ends
    for r in routes.values():
        util.addDepotAtEnds(depot, r)

    # totalDist = 0
    # for k,v in routes.iteritems():
    #     totalDist += util.calculateRouteCost(v)
    #     print(k,"-",v)
    # print(totalDist)

    return routes

#compute Savings for depot and i,j where i <> j
def computeSaving(depot, i,j):
    iDepot = util.manhattanDistance(i, depot)
    jDepot = util.manhattanDistance(depot, j)
    ijDist = util.manhattanDistance(i, j)
    
    return (iDepot + jDepot - ijDist)
    
#def distDepot

def allCustomersConsidered(customerServed):
    for val in customerServed.values():
        if val == False:
            return False
    return True

def inPrevious(new,existing):
    start = existing[0]
    end = existing[len(existing)-1]
    if new == start:
        return 1
    elif new == end:
        return 0
    else:
        return -1

def capacityValid(existing, new, customerPosDemand):
    totalCap = customerPosDemand[new]
    for c in existing:
        totalCap+=customerPosDemand[c]
    return totalCap <= vehicleCap

def isServed(c):
    return customerServed[c]

def hasBeenServed(c):
    customerServed[c] = True   

