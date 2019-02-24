
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        # Student code goes here
        # Student code goes here
        # DFS implemented using stack (LIFO)
        # look at starting condition
        # consider the movable moves from first to last
        # for every movable look at its movables
        # every time you move to another thing you check if it is winning condition

        # fill the tree with game states
        # look at top node
        # get the movables, make new game state, append to children
        # check if currentState == victory state --> return true
        # if self.currentState.state == self.victoryCondition:
        #    return True
        # if not at victory condition
        # looping through movables
        # get movables and loop through as long as curr.children is empty and there are movables
        # loop through movables -> make move to child --> make new gameState (depth + 1) --> set newState.parent to self.current state --> append new state to children of current
        # reverseMove

        moved = False
        # if we have reached the victory state --> return true
        if self.currentState.state == self.victoryCondition:
            return True

        # look at all of the possible moves and add the children (movables)
        for move in self.gm.getMovables():
            # for every move, make the move and get the resulting game state
            self.gm.makeMove(move)
            newGameState = self.gm.getGameState()
            newChild = GameState(newGameState, self.currentState.depth + 1, move)
            # if the move will not bring you back to the parent state --> populate this child with information
            if not self.currentState.parent or not newGameState == self.currentState.parent.state:
                # add child to children array
                self.currentState.children.append(newChild)
                # update the parent of this new child
                newChild.parent = self.currentState
            self.gm.reverseMove(move)

        # actually make the move
        while self.currentState.nextChildToVisit < len(self.currentState.children):
            # if the next child to visit has not been visited yet --> visit it
            if self.currentState.children[self.currentState.nextChildToVisit] not in self.visited:
                # update move
                moved = True
                # make the move to get you to this child
                self.gm.makeMove(self.currentState.children[self.currentState.nextChildToVisit].requiredMovable)
                self.currentState = self.currentState.children[self.currentState.nextChildToVisit]
                # update visited
                self.visited[self.currentState] = True
                if self.victoryCondition == self.currentState.state:
                    return True
                else:
                    return False
            self.currentState.nextChildToVisit = self.currentState.nextChildToVisit + 1

        # if we never find a child to visit next --> go back to the parent
        else:
            self.currentState = self.currentState.parent
            self.gm.reverseMove(self.currentState.requiredMovable)


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.bfsQ = deque()
        self.bfsQ.append(self.currentState)
        self.front = 0

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        # Student code goes here