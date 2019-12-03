from operator import itemgetter
# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def isPathToGoal(path, goal):
  for node in path:
    if(goal == node):
      return True
  return False

def bfs(graph, start, goal):
    agenda = [ [start ]]           
    while agenda:      
      path = agenda.pop()
      current = path[0]
      if isPathToGoal(path, goal):
        path.reverse()
        return path
      else:
        nodes = graph.get_connected_nodes(current)
        for n in nodes:
          if n not in path:
            newPath = [n] + path
            agenda = [newPath] + agenda
    return None

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    agenda = [ [start ]]           
    while agenda:      
      path = agenda.pop()
      current = path[0]
      if isPathToGoal(path, goal):
        path.reverse()
        return path
      else:
        nodes = graph.get_connected_nodes(current)
        for n in nodes:
          if n not in path:
            newPath = [n] + path
            agenda.append(newPath)       
    return None


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    extended = []
    agenda = [ [start ] ]           
    while agenda:      
      path = agenda.pop()
##      currentHeuristic = hPath[0]
      ##path = hPath[1]
      currentNode = path[0]
      if isPathToGoal(path, goal):
        path.reverse()
        return path
      else:
        nodes = graph.get_connected_nodes(currentNode)
        toBeSorted = []
        extended.append(currentNode)
        for n in nodes:
          if n not in path and n not in extended:            
            lengthToNode = graph.get_heuristic(n, goal) ## + currentHeuristic
            newPath = [n] + path
            lengthAndPath = (lengthToNode, newPath)
            toBeSorted.append(lengthAndPath)
        toBeSorted.sort(key=itemgetter(0),reverse=True)
        nodesOnly = map(lambda tup: tup[1], toBeSorted)
        for n in nodesOnly:
          agenda.append(n)
    return None

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):    
    agenda = [ [ [ start ] ]]     
    while agenda:
      paths = agenda.pop()
      if not paths: 
        return paths
##      currentHeuristic = hPath[0]
      ##path = hPath[1]
      ##currentNode = path[0]
      for path in paths: 
        if isPathToGoal(path, goal):
          path.reverse()
          return path
      else:
        toBeSorted = []
        for path in paths:
          currentNode = path[0]
          nodes = graph.get_connected_nodes(currentNode)                 
          for n in nodes:
            if n not in path:
              lengthToNode = graph.get_heuristic(n, goal) ## + currentHeuristic
              newPath = [n] + path
              lengthAndPath = (lengthToNode, newPath)
              toBeSorted.append(lengthAndPath)
        toBeSorted.sort(key=itemgetter(0))
        nodesOnly = map(lambda tup: tup[1], toBeSorted)
        topOnly = nodesOnly[:beam_width]     
        agenda.append(topOnly)
    return None

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    if len(node_names) < 2:
      return 0
    acc = 0
    for i in range(0, len(node_names)-1):
      edge = graph.get_edge(node_names[i], node_names[i+1])
      acc += edge.length
    return acc

def branch_and_bound(graph, start, goal):
    agenda = [ (0, [start]) ]
    extended = []
    while agenda:
      agenda.sort(reverse=True)
      path = agenda.pop()
      if isPathToGoal(path[1], goal):
          path[1].reverse()
          return path[1]
      else:
        currentLength = path[0]
        currentPath = path[1]
        currentNode = currentPath[0]
        nodes = graph.get_connected_nodes(currentNode)        
        for n in nodes:
          extended.append(n)
          if n not in currentPath:
            length = path_length(graph, [currentNode, n])            
            newLength = length + currentLength
            newPath = [n] + currentPath
            lengthAndPath = (newLength, newPath)
            containsShorterPath = False
            for path in agenda:
              if path[1][0] == lengthAndPath[1][0] and path[0] <= lengthAndPath[0]:
                containsShorterPath = True
            if not containsShorterPath:
              agenda.append(lengthAndPath)            
    return None

def a_star(graph, start, goal):
    agenda = [ (0, [start]) ]
    extended = []
    while agenda:
      agenda.sort(reverse=True)
      path = agenda.pop()
      if isPathToGoal(path[1], goal):
          path[1].reverse()
          return path[1]
      else:
        currentLengthAndEstimate = path[0]
        currentPath = path[1]
        currentNode = currentPath[0]
        nodes = graph.get_connected_nodes(currentNode)        
        for n in nodes:
          extended.append(n)
          if n not in currentPath:
            length = path_length(graph, [currentNode, n])
            estimate = graph.get_heuristic(n, goal)       
            newLength = length + estimate + currentLengthAndEstimate 
            newPath = [n] + currentPath
            lengthAndPath = (newLength, newPath)
            containsShorterPath = False
            for path in agenda:
              if path[1][0] == lengthAndPath[1][0] and path[0] <= lengthAndPath[0]:
                containsShorterPath = True
            if not containsShorterPath:
              agenda.append(lengthAndPath)
    return None


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):    
  for node in graph.nodes:
    length = path_length(graph, branch_and_bound(graph, node, goal))
    heuristic = graph.get_heuristic(node, goal)
    if heuristic > length:
      return False
  return True

def is_consistent(graph, goal):
    if not is_admissible(graph,goal):
        return False
    for edge in graph.edges:
        if graph.get_heuristic(edge.node1,goal)>edge.length+graph.get_heuristic(edge.node2,goal):
            return False
        if graph.get_heuristic(edge.node2,goal)>edge.length+graph.get_heuristic(edge.node1,goal):
            return False
    if graph.get_heuristic(goal,goal) !=0:
        return False
    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '10'
WHAT_I_FOUND_INTERESTING = 'asdf'
WHAT_I_FOUND_BORING = 'asdf'
