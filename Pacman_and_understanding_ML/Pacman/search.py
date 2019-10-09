# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    # 1. Our DFS uses stack as fringe data structure
    # 2. We create an empty initList initially, this list stores the directions that we took to reach this position
    #    Hence it is initally null.
    # 3. We create a tuple of start state, direction list (initList) and cost (0 initially, used for UCS and A*), and send to generic search method
    fringe = util.Stack() # our fringe list
    initList = []         # stores the directions taken to reach this node
    root = (problem.getStartState(),initList,0) # the root (base position)
    fringe.push(root)
    return solveTheTraversalProblem(problem,0,fringe)
    #util.raiseNotDefined()
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    # 1. Our BFS uses queue as fringe data structure
    # 2. We create an empty initList initially, this list stores the directions that we took to reach this position
    #    Hence it is initally null.
    # 3. We create a tuple of start state, direction list (initList) and cost (0 initially, used for UCS and A*), and send to generic search method
    fringe = util.Queue()
    initList = []
    root = (problem.getStartState(), initList, 0)
    fringe.push(root)
    return solveTheTraversalProblem(problem, 1, fringe)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # 1. Our UCS uses priority queue as fringe data structure
    # 2. We create an empty initList initially, this list stores the directions that we took to reach this position
    #    Hence it is initally null.
    # 3. We create a tuple of start state, direction list (initList) and cost (0 initially, used for UCS and A*), and send to generic search method
    fringe = util.PriorityQueue()
    initList = []
    root = (problem.getStartState(), initList, 0)
    fringe.push(root,0)
    return solveTheTraversalProblem(problem, 2, fringe)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # 1. Our A* uses priority queue as fringe data structure
    # 2. We create an empty initList initially, this list stores the directions that we took to reach this position
    #    Hence it is initally null.
    # 3. We create a tuple of start state, direction list (initList) and cost (0 initially, used for UCS and A*), and send to generic search method
    fringe = util.PriorityQueue()
    initList = []
    root = (problem.getStartState(), initList, heuristic(problem.getStartState(),problem))
    fringe.push(root,heuristic(problem.getStartState(),problem))
    return solveTheTraversalProblem(problem, 3, fringe, heuristic)


# This is the generic search method written for DFS, BFS, UCS and A*
def solveTheTraversalProblem(problem,type,fringe,heuristic=nullHeuristic):

    visitedList = [] # stores the nodes that have been visited
    returnList = []  # stores the directions that will be finally returned to caller search method
    while(fringe.isEmpty() == False):
        parent = fringe.pop()
        #print "popped: ",parent
        if(problem.isGoalState(parent[0]) == True): # add all directions to returnList from the tuple's second argument (initList) once goal is reached
            returnList = parent[1]
            break
        if parent[0] not in visitedList:  # do next operations only if these operations were never done before on this node
            childList = problem.getSuccessors(parent[0])
            for child in childList:
                if child[0] not in visitedList: # get all the children of this node, and if unvisited, calculate the cost of visiting and add to P.Queue
                    path = parent[1] + [child[1]]
                    #print "adding child: , ", childNode
                    cost = 0
                    if(type == 3): # This case is for A* search, we add g(x) + h(x) but substract the heuristic value added of parent to the node already
                        cost = parent[2]+child[2]+heuristic(child[0],problem)-heuristic(parent[0],problem)
                        childNode = (child[0], path, cost)
                        fringe.update(childNode,cost)
                    elif(type == 2): # Case for UCS, add to fringe list with the calculated cost. The Update function does the job of add too
                        cost = parent[2] + child[2]
                        childNode = (child[0], path, cost)
                        fringe.update(childNode,cost)
                    else:
                        childNode = (child[0], path, child[2])
                        fringe.push(childNode)
            visitedList.append(parent[0])

    return returnList

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
