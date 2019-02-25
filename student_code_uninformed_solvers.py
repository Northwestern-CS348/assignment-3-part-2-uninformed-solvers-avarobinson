from solver import *
from collections import deque

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
        self.q = deque()

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
        if self.currentState.state == self.victoryCondition:
            return True
        else:
            self.visited[self.currentState] = True

        # if we have not seen this state before --> add it to the queue
        if self.currentState not in self.q and self.currentState:
            self.q.append(self.currentState)

        if self.gm.getMovables():
            for move in self.gm.getMovables():
                #make the move and make a new game state
                self.gm.makeMove(move)
                new_state = self.gm.getGameState()
                new_game_state = GameState(new_state, self.currentState.depth + 1, move)
                #update the parent
                new_game_state.parent = self.currentState
                #add the new state to the children
                self.currentState.children.append(new_game_state)
                if new_game_state not in self.visited:
                    self.visited[new_game_state] = False
                self.gm.reverseMove(move)

            for c in self.currentState.children:
                if c not in self.q and not self.visited[c]:
                    self.q.append(c)

        # need to remove the current node
        self.q.popleft()

        path = []
        currentstate = self.q[0]
        x = 0

        # reversing all the way back to the top parent, changes current state
        while self.currentState.parent:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        # filling the path array with all the moves needed to get back to the parent, changes the queue state
        while currentstate.parent:
            path.insert(0, currentstate.requiredMovable)
            currentstate = currentstate.parent

        # make all the moves we just stored in path that are required to get down to first queue
        while x < len(path):
            self.gm.makeMove(path[x])
            x += 1
        self.currentState = self.q[0]

        if self.currentState.state == self.victoryCondition:
            return True
        else:
            return False


