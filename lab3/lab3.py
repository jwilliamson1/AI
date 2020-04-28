# 6.034 Fall 2010 Lab 3: Games
# Name: <Your Name>
# Email: <Your Email>

from util import INFINITY

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 3

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 2

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(basic_player, human_player)

## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

# TODO: handle gaps in long chain, and do we need more pieces vertically to get there?      
# TODO: do we care what the oponent is doing or does alphabeta cover that?
def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """    
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -1000
        return score
    else:
        currentPlayerId = board.get_current_player_id()
        otherPlayerId = board.get_other_player_id()

        score = scoreBoard(board, currentPlayerId, otherPlayerId)
        return score
        # positionsAvailable = 42 - board.num_tokens_on_board()

        # #is current player losing on this board?
        # if (positionsAvailable < 21 and score < 0):
        #   blockingScore = scoreBoard(board, otherPlayerId, currentPlayerId)
        #   assert blockingScore != None
        #   return blockingScore * -1
        # else:
        #   assert score != None
        #   return score        

## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.
def alphabeta_max_value(board, depth, alpha, beta, eval_fn,
                             get_next_moves_fn=get_all_next_moves,
                             is_terminal_fn=is_terminal):
    """
    Minimax helper function: Return the minimax value of a particular board,
    given a particular depth to estimate to
    """
    if is_terminal_fn(depth, board):
        return eval_fn(board)

    best_val = NEG_INFINITY
    
    for move, new_board in get_next_moves_fn(board):
        best_val = -1 * max(best_val, alphabeta_min_value(new_board, depth-1, alpha, beta, eval_fn,
                                            get_next_moves_fn, is_terminal_fn))
        alpha = max(best_val, alpha)
        if (alpha >= beta):
          return alpha

    return best_val

def alphabeta_min_value(board, depth, alpha, beta, eval_fn,
                            get_next_moves_fn=get_all_next_moves,
                            is_terminal_fn=is_terminal):
  """
  Minimax helper function: Return the minimax value of a particular board,
  given a particular depth to estimate to
  """
  if is_terminal_fn(depth, board):
      return eval_fn(board)

  best_val = INFINITY
  
  for move, new_board in get_next_moves_fn(board):
      best_val = min(best_val, alphabeta_max_value(new_board, depth-1, alpha, beta, eval_fn,
                                          get_next_moves_fn, is_terminal_fn))
      beta = min(best_val, beta)
      if(alpha >= beta):
        return beta

  return best_val

def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
		      is_terminal_fn=is_terminal,
          verbose = True,
          alpha=NEG_INFINITY,
          beta=INFINITY):
    """
    Do a minimax search to the specified depth on the specified board.

    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree; see "focused_evaluate" in the lab for an example

    Returns an integer, the column number of the column that the search determines you should add a token to
    """
    best_val = None
    
    for move, new_board in get_next_moves_fn(board):
        val = -1 * alphabeta_max_value(new_board, depth-1, alpha, beta, eval_fn,
                                            get_next_moves_fn,
                                            is_terminal_fn)
        if best_val == None or val > best_val[0]:
            best_val = (val, move, new_board)
            
    # if verbose:
    #     print "ALPHA_BETA: Decided on column %d with rating %d" % (best_val[1], best_val[0])

    return best_val[1]

## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
alphabeta_player = lambda board: alpha_beta_search(board,
                                                   depth=8,
                                                   eval_fn=focused_evaluate)

## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
#run_game(human_player, alphabeta_player)

## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

def better_evaluate(board):
  if board.is_game_over():
      # If the game has been won, we know that it must have been
      # won or ended by the previous move.
      # The previous move was made by our opponent.
      # Therefore, we can't have won, so return -1000.
      # (note that this causes a tie to be treated like a loss)
      score = -1000
      return score
  else:
      currentPlayerId = board.get_current_player_id()
      otherPlayerId = board.get_other_player_id()

      score = scoreBoard(board, currentPlayerId, otherPlayerId)
      return score
      # positionsAvailable = 42 - board.num_tokens_on_board()

      # #is current player losing on this board?
      # if (positionsAvailable < 21 and score < 0):
      #   blockingScore = scoreBoard(board, otherPlayerId, currentPlayerId)
      #   assert blockingScore != None
      #   return blockingScore * -1
      # else:
      #   assert score != None
      #   return score       
      #  
def onEdge(listOfTuples):
  for tup in listOfTuples:
    return tup[0] == 0 or tup[1] == 0 or tup[1] == 6
# me = playerNo 2
def scoreBoard(board, currentPlayerId, otherPlayerId):
    score = 0
    #opChains shouldn't change
    cpChains = filter(lambda x: len(x) > 1, board.chain_cells(currentPlayerId))
    opChains = filter(lambda x: len(x) > 1, board.chain_cells(otherPlayerId))

    aggScore = evalChain(board, cpChains, 0, 10)

    defScore = evalChain(board, opChains, currentPlayerId, 20)

    score += aggScore
    score += defScore
    #print("eval chain scores")
  # Prefer having your pieces in the center of the board.
  # TODO: handle gaps in long chain, and do we need more pieces vertically to get there?      
  # TODO: do we care what the oponent is doing or does alphabeta cover that?
    for row in range(6):      
        for col in range(7):
                #subtract more from current player if farther from middle
            if board.get_cell(row, col) == currentPlayerId:
                score -= abs(3-col)
                score -= abs(2-row)
                #add more to current player if opponent is farther from middle
            elif board.get_cell(row, col) == otherPlayerId:
                score += abs(3-col)
                score += abs(2-row)

    return score
def evalChain(board, otherPlayerNewChains, expectedAdjacentPlayerId, factor):
  score = 0
  for otherPlayerChain in otherPlayerNewChains:
      chainLength = len(otherPlayerChain)
      # only bother with chains bigger than 0
      if chainLength > 1:
          # get ends
          endX = otherPlayerChain[0][0]
          endY = otherPlayerChain[0][1]
          startX = otherPlayerChain[chainLength-1][0]
          startY = otherPlayerChain[chainLength-1][1]
      #Horizontal
          if startX == endX:
              if startY > 0:
                  startAdjacent = board.get_cell(startX, startY-1)
                  #check if opponent is next to end
                  if startAdjacent == expectedAdjacentPlayerId:
<<<<<<< HEAD
                      score += factor 
              if endY < 6:
                  endAdjacent = board.get_cell(endX, endY+1)
                  if  endAdjacent == expectedAdjacentPlayerId:
                      score += factor 
=======
                      score += factor ^ chainLength
              if endY < 6:
                  endAdjacent = board.get_cell(endX, endY+1)
                  if  endAdjacent == expectedAdjacentPlayerId:
                      score += factor ^ chainLength
>>>>>>> 73bbcea7984af969313b3c70aeda7b42dc62d476
          elif startY == endY:
              if startX > 0:
                  startAdjacent = board.get_cell(startX-1, startY)
                  #check if opponent is next to end
                  if startAdjacent == expectedAdjacentPlayerId:
<<<<<<< HEAD
                      score += factor 
=======
                      score += factor ^ chainLength
>>>>>>> 73bbcea7984af969313b3c70aeda7b42dc62d476
              # if endX < 5:
              #     endAdjacent = board.get_cell(endX+1, endY)
              #     if  endAdjacent == currentPlayerId:
              #         score += factor
              #Diagonal lower left to upper right
          elif startX > endX:
              if endY < 6 and endX > 0:
                  startAdjacent = board.get_cell(endX-1, endY+1)
                  if startAdjacent == expectedAdjacentPlayerId:
<<<<<<< HEAD
                      score += factor 
              if startY > 0 and startX < 5:
                  startAdjacent = board.get_cell(endX+1, endY-1)
                  if startAdjacent == expectedAdjacentPlayerId:
                      score += factor 
=======
                      score += factor ^ chainLength
              if startY > 0 and startX < 5:
                  startAdjacent = board.get_cell(endX+1, endY-1)
                  if startAdjacent == expectedAdjacentPlayerId:
                      score += factor ^ chainLength
>>>>>>> 73bbcea7984af969313b3c70aeda7b42dc62d476
              #Diagonal upper left to lower right
          elif startX < endX:
            if startX > 0 and startY > 0:
                  startAdjacent = board.get_cell(startX-1, startY-1)
                  if startAdjacent == expectedAdjacentPlayerId:
<<<<<<< HEAD
                      score += factor 
            if endX < 5 and endY < 6:
                startAdjacent = board.get_cell(endX+1, endY+1)
                if startAdjacent == expectedAdjacentPlayerId:
                    score += factor 
=======
                      score += factor ^ chainLength
            if endX < 5 and endY < 6:
                startAdjacent = board.get_cell(endX+1, endY+1)
                if startAdjacent == expectedAdjacentPlayerId:
                    score += factor ^ chainLength
>>>>>>> 73bbcea7984af969313b3c70aeda7b42dc62d476
          else: raise Exception("should not be here. ")
  return score
# Comment this line after you've fully implemented better_evaluate
#better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    # better evaluate from player 2
    print "%s => %s" %(test_board_2, better_evaluate(test_board_2))

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
#run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
#run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])
    
def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)
    
## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = (False)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "8"
WHAT_I_FOUND_INTERESTING = "stuff"
WHAT_I_FOUND_BORING = "stuff"
NAME = "aasdf"
EMAIL = "asdf@asdf.org"

