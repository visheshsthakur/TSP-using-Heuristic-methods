import veroviz as vrv
import random
import numpy as np
import math
import time

# In UBSERID_tsp.py
def solveTSP_SA(nodesDF, costDict, timeLimit):
    startNode = 1
    def solve_tsp_nn(startNode, costDict, nodesDF): 
        nn_route = []
        nn_route.append(startNode)
        unvisitedNodes = list(nodesDF[nodesDF['id'] != startNode]['id'])
        i = startNode

        while len(unvisitedNodes) > 0:
            minTime = float('inf')
            for j in unvisitedNodes:
                if (costDict[i,j] < minTime):
                    nextNode = j
                    minTime = costDict[i,j]

            i = nextNode
            nn_route.append(nextNode)
            unvisitedNodes.remove(nextNode)

        nn_route.append(startNode)

        return nn_route
    # Initialize by calling your nearest neighbor function
    nn_route = solve_tsp_nn(startNode, costDict, nodesDF)

    def tsp_cost(route, costDict):
        icost = []
    
        i = route[0]
        for j in route[1:]:
            icost.append(costDict[i,j])
        
        cost = np.sum(icost)
        return cost
    #NnCost = tsp_cost(nn_route, costDict)
    
    def tsp_neighbor(route):
        # You should document this function to explain what's happening
    
        a = random.randint(0,len(route)-3)
        b = random.randint(a+1, len(route)-2)
    
        newRoute = []
        newRoute.extend(route[0:a])
        
        subtour = route[a:b+1]
        subtour.reverse()
        newRoute.extend(subtour)
    
        newRoute.extend(route[b+1:len(route)-1])
    
        newRoute.append(newRoute[0])
    
        return newRoute
    
    initialRoute = tsp_neighbor(nn_route)
    
    def SimAnnealing(nodesDF, costDict, Ctime):
        Tcurr = 100000
        startNode = 1
        delta = 1.00002
        Tf = 1
        startTime = time.time()
        I = 10
        Xcount = initialRoute
        Xcurrent = solve_tsp_nn(startNode, costDict, nodesDF)
        ZXcurrent = tsp_cost(Xcurrent, costDict)
        ZXbest = tsp_cost(Xcurrent, costDict)
        Xbest = 0
        while ((Tcurr > Tf) and (time.time() - startTime <= Ctime)):
            for i in range(I):
                Xcount = tsp_neighbor(nn_route)
                ZXcount = tsp_cost(Xcount, costDict)
                #print(i)
                if ZXcount < ZXcurrent: #1
                    Xcurrent = Xcount
                    ZXcurrent = ZXcount
                    #print("1 is working")
                else: #2
                    delC = ZXcount - ZXcurrent
                    if random.random() <= np.exp(-delC/Tcurr):
                        Xcurrent = Xcount
                        ZXcurrent = ZXcount
                        #print("2 is working")
                if ZXcurrent < ZXbest: #3
                    ZXbest = ZXcurrent
                    Xbest = Xcurrent
                #print("3 is working")
            Tcurr = Tcurr/delta
           #print(ZXbest)
        return ZXbest, Xbest
    ZX_best, X_best = SimAnnealing(nodesDF, costDict, timeLimit)
    
    # Your function should return a VeRoViz "assignments" dataframe.
    # Fortunately, VeRoViz provides a function to make this very easy:
    assignmentsDF = vrv.createAssignmentsFromNodeSeq2D(
        nodeSeq          = X_best,        # This is what you should have found above, via SA.
        nodes            = nodesDF,       # This is an input to your solveTSP_SA() function
        routeType        = 'fastest',     # Leave this as 'fastest'
        dataProvider     = 'ORS-online',  # Leave this as 'ORS-online'
        dataProviderArgs = {'APIkey' : '5b3ce3597851110001cf62486656f8c18ab44be2953c9052af90bf5d'})    # You'll need to replace ORS_API_KEY with your actual key

    # See https://veroviz.org/docs/veroviz.createAssignments.html#veroviz.createAssignments.createAssignmentsFromNodeSeq2D
    # for more info on this function.
    
    return assignmentsDF