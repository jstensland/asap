# refactor to make some methods private, that should never be called on a graph alone.
# refactor to re-order i, j and k such that in the end you can just find the mine for the last
# 2D matrix

class DirectedGraph(object):

        def __init__(self, edgeList, nodeCount, edgeCount):
            self.edgeList = edgeList
            self.nodeCount = nodeCount
            self.edgeCount = edgeCount

            self.pathLengthsMatrix = []
            self.finalPathsIndex = self.nodeCount % 2

        def __str__(self):
            edgeStrList = list(map(str, self.edgeList))
            nodeCount = 'Node Count: ' + str(self.nodeCount) + ' \n'
            edgeCount = 'Edge Count: ' + str(self.edgeCount) + ' \n'
            edges = 'Edges List: \n' + '\n'.join(edgeStrList) + '\n'
            objectId = self.__repr__()
            return nodeCount + edgeCount + edges + objectId

        def findShortestShortestPath(self):
            self.asapFloydWarshall()
            if self.negativeCycleCheck():
                return "negative Cycle!"
            else:
                return self.shortestShortestPathFW()

        def negativeCycleCheck(self):
            negativeCycle = False
            for i in range(self.nodeCount):
                if self.pathLengthsMatrix[i][i][self.finalPathsIndex] is not None:
                    if self.pathLengthsMatrix[i][i][self.finalPathsIndex] < 0:
                        negativeCycle = True
            return negativeCycle

        def shortestShortestPathFW(self):
            shortest = 100000000
            for i in range(self.nodeCount):
                for j in range(self.nodeCount):
                    if self.pathLengthsMatrix[i][j][self.finalPathsIndex] is not None:
                        if self.pathLengthsMatrix[i][j][self.finalPathsIndex] < shortest:
                            shortest = self.pathLengthsMatrix[i][j][self.finalPathsIndex]
            return shortest

        def asapFloydWarshall(self):
            # initialize Matrix
            print("start to put in zeros and infinities")
            # k is round, starting with zero and including through all nodes
            # thus k is the new node being introduced, which can be found at k-1 in the array
            self.pathLengthsMatrix = [[[self.initializeArrayValue(i, j, k)
                                        for k in range(2)]
                                       for j in range(self.nodeCount)]
                                      for i in range(self.nodeCount)]
            print("put in zeros and infinities")
            self.addInitialEdgeValues()
            print("Matrix initialized")

            self.calculatePathLengthsMatrix()
    #        pprint.pprint(self.pathLengthsMatrix)

        def initializeArrayValue(self, i, j, k):
            initialValue = None
            if i == j and k == 0:
                initialValue = 0
            return initialValue

        def addInitialEdgeValues(self):
            for edge in self.edgeList:
                currentEdgeValue = self.pathLengthsMatrix[edge[0] - 1][edge[1] - 1][0]
                if currentEdgeValue == None or currentEdgeValue > edge[2]:
                    self.pathLengthsMatrix[edge[0]-1][edge[1]-1][0] = edge[2]

        def calculatePathLengthsMatrix(self):
            for k in range(1, self.nodeCount + 1):
                if k % 10 == 0:
                    print("round:" + str(k))
                for i in range(self.nodeCount):
                    for j in range(self.nodeCount):

                        self.pathLengthsMatrix[i][j][k % 2] = self.newPathLength(i, j, k)


        def newPathLength(self, i, j, k):
            currentRound = k % 2
     #       print (currentRound)
            previousRound = (k - 1 ) % 2

            #if nodes not connected and k doesn't connect them, still unconnected.
            if self.pathLengthsMatrix[i][j][previousRound] != None:
                case1 = self.pathLengthsMatrix[i][j][previousRound]
            else:
                case1 = None

            if self.pathLengthsMatrix[i][k-1][previousRound] != None and self.pathLengthsMatrix[k-1][j][previousRound] != None:
                case2 = self.pathLengthsMatrix[i][k-1][previousRound] + self.pathLengthsMatrix[k-1][j][previousRound]
            else:
                case2 = None

            if case1 == None and case2 == None:
                return None
            elif case1 == None:
                return case2
            elif case2 == None:
                return case1
            else:
    #            print (min(case1, case2))
                return min(case1, case2)
