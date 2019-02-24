from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        peg1=[]
        peg2=[]
        peg3=[]

        #finding what is on peg1
        listOfBindings=self.kb.kb_ask(parse_input('fact: (on ?disk peg1)')) #returns a list of bindings
        #for each element in the list of bindigns we want to get the constant
        if listOfBindings:
            for bindings in listOfBindings:
                binding = bindings.bindings_dict['?disk']  # return a binding object
                diskNumber = int(binding[-1])
                peg1.append(diskNumber)

        #finding what is on peg2
        listOfBindings = self.kb.kb_ask(parse_input('fact: (on ?disk peg2)'))  # returns a list of bindings
        # for each element in the list of bindigns we want to get the constant
        if listOfBindings:
            for bindings in listOfBindings:
                binding=bindings.bindings_dict['?disk'] #return a binding object
                diskNumber = int(binding[-1])
                peg2.append(diskNumber)

        #finding whats on peg3
        listOfBindings = self.kb.kb_ask(parse_input('fact: (on ?disk peg3)'))  # returns a list of bindings
        # for each element in the list of bindigns we want to get the constant
        if listOfBindings:
            for bindings in listOfBindings:
                binding = bindings.bindings_dict['?disk']  # return a binding object
                diskNumber = int(binding[-1])
                peg3.append(diskNumber)

        game_state=(tuple(sorted(peg1)), tuple(sorted(peg2)), tuple(sorted(peg3)))
        return game_state

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        # Student code goes here
        matches = match(movable_statement, (self.produceMovableQuery()).statement)
        if matches:

            disk = matches.bindings[0].constant.element # disk that we are trying to move
            start = matches.bindings[1].constant.element # starting peg
            end = matches.bindings[2].constant.element # end peg

            # retract on statement
            self.kb.kb_retract(parse_input('fact: (on ' + disk + ' ' + start + ')'))
            # retract the top statement
            self.kb.kb_retract(parse_input('fact: (top ' + disk + ' ' + start + ')'))

            if not self.kb.kb_ask(parse_input('fact: (above ' + disk + ' ?diskb)')):  # if start will b empty
                self.kb.kb_assert((parse_input('fact: (empty ' + start + ')')))  # make the start peg empty
            else: # if the start is not empty then we have to assert a new top on the start peg
                listOfBindings = self.kb.kb_ask(parse_input('fact: (above ' + disk + ' ?diskb)'))
                new_top = listOfBindings[0].bindings_dict['?diskb']  # return a disk object
                self.kb.kb_assert(parse_input('fact: (top ' + new_top + ' ' + start + ')'))  # assert new top for start peg
                self.kb.kb_retract(parse_input('fact: (above ' + disk + ' ' + new_top + ')'))

            # if the peg we are moving to is empty then we have to retract the empty fact
            if self.kb.kb_ask(parse_input('fact: (empty ' + end + ')')):
                self.kb.kb_retract(parse_input('fact: (empty ' + end + ')'))
                #assert new on statement
                self.kb.kb_assert(parse_input('fact: (on ' + disk + ' ' + end + ')'))
                #assert new top statement for end peg
                self.kb.kb_assert(parse_input('fact: (top ' + disk + ' ' + end + ')'))

            #if the peg we are moving to is not empty then we must retract the old top and assert a new one
            else:
                #retract the old top on the end peg
                listOfBindings = self.kb.kb_ask(parse_input('fact: (top ?disk ' + end + ')'))
                old_top = listOfBindings[0].bindings_dict['?disk']
                self.kb.kb_retract(parse_input('fact: (top ' + old_top + ' ' + end + ')'))

                #make new top on the target peg
                # assert new on statement
                self.kb.kb_assert(parse_input('fact: (on ' + disk + ' ' + end + ')'))
                # assert new top statement for end peg
                self.kb.kb_assert(parse_input('fact: (top ' + disk + ' ' + end + ')'))
                self.kb.kb_assert(parse_input('fact: (above ' + disk + ' ' + old_top))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        row1 = [-1, -1, -1]
        row2 = [-1, -1, -1]
        row3 = [-1, -1, -1]

        # row1
        listOfBindings = self.kb.kb_ask(parse_input('fact: (position ?tile ?x pos1'))
        for binding in listOfBindings:
            tileNumber = int((binding.bindings_dict['?tile'])[-1])
            positionBinding = self.kb.kb_ask(parse_input('fact: (position tile' + str(tileNumber) + ' ?pos pos1'))
            tile_x_pos = int((positionBinding[0].bindings_dict['?pos'])[-1])
            if not tileNumber == 0:
                row1[tile_x_pos - 1] = tileNumber
        # row2
        listOfBindings = self.kb.kb_ask(parse_input('fact: (position ?tile ?x pos2'))
        for binding in listOfBindings:
            tileNumber = int((binding.bindings_dict['?tile'])[-1])
            positionBinding = self.kb.kb_ask(parse_input('fact: (position tile' + str(tileNumber) + ' ?pos pos2'))
            tile_x_pos = int((positionBinding[0].bindings_dict['?pos'])[-1])
            if not tileNumber == 0:
                row2[tile_x_pos - 1] = tileNumber

        # row3
        listOfBindings = self.kb.kb_ask(parse_input('fact: (position ?tile ?x pos3'))
        for binding in listOfBindings:
            tileNumber = int((binding.bindings_dict['?tile'])[-1])
            positionBinding = self.kb.kb_ask(parse_input('fact: (position tile' + str(tileNumber) + ' ?pos pos3'))
            tile_x_pos = int((positionBinding[0].bindings_dict['?pos'])[-1])
            if not tileNumber == 0:
                row3[tile_x_pos - 1] = tileNumber

        game_state = (tuple(row1), tuple(row2), tuple(row3))
        return game_state

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """

        if self.isMovableLegal(movable_statement):
            matches = match(movable_statement, (self.produceMovableQuery()).statement)
            tile = matches.bindings[0].constant.element
            position1 = matches.bindings[1].constant.element
            position2 = matches.bindings[2].constant.element
            position3 = matches.bindings[3].constant.element
            position4 = matches.bindings[4].constant.element

            # listOfBindings = self.kb.kb_ask(parse_input('fact: (position ?tile ' + position3 + ' ' + position4 + ')'))
            # tile2 = listOfBindings[0].bindings_dict['?tile']  # returns the swapping tile

            self.kb.kb_retract(parse_input('fact: (position ' + tile + ' ' + position1 + ' ' + position2 + ')'))
            self.kb.kb_retract(parse_input('fact: (position tile0 ' + position3 + ' ' + position4 + ')'))

            self.kb.kb_assert(parse_input('fact: (position ' + tile + ' ' + position3 + ' ' + position4 + ')'))
            self.kb.kb_assert(parse_input('fact: (position tile0 ' + position1 + ' ' + position2 + ')'))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
