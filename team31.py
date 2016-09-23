import random
import sys
import copy
import time


class Player31:
    """
    Class to Deal with the agent in game
    """

    def __init__(self):
        """ Default Constructor  """
        self.ply = 5
        self.num = 0
        self.cntp = 0
        self.cnto = 0
        pass

    def get_free_cells(self, board, blocks_allowed, block_status):
        """

        :param board:  board input
        :param blocks_allowed: list containing numbers of blocks which are allowed
        :return: list of cells which are available for a move
        """

        cells = []
        for block in blocks_allowed:
            startx = block / 3
            starty = block % 3
            for i in range(startx * 3, startx * 3 + 3):
                for j in range(starty * 3, starty * 3 + 3):
                    if board[i][j] == '-':
                        cells.append((i, j))
        if len(cells) == 0:
            # print "Used Free Move"
            new_blocks_allowed = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            for block in new_blocks_allowed:
                startx = block / 3
                starty = block % 3
                for i in range(startx * 3, startx * 3 + 3):
                    for j in range(starty * 3, starty * 3 + 3):
                        if board[i][j] == '-' and block_status[block] == '-':
                            cells.append((i, j))
        return cells

    def free_move(self, block):
    	""" Function that deals with the case of a free move """	
        blocks_allowed = []
        for i in range(9):
            if block[i] == '-':
                blocks_allowed.append(i);
        return blocks_allowed

    def get_allowed_blocks(self, block, old_move):
        """

        :param block: list containg status of each block
        :param old_move: previous move
        :return: list of block numbres which are allowed
        """
        blocks_allowed = []
        if old_move == (-1, -1):
            blocks_allowed = self.free_move(block)
        elif old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
            blocks_allowed = [1, 3]
        elif old_move[0] % 3 == 0 and old_move[1] % 3 == 2:
            blocks_allowed = [1, 5]
        elif old_move[0] % 3 == 2 and old_move[1] % 3 == 0:
            blocks_allowed = [3, 7]
        elif old_move[0] % 3 == 2 and old_move[1] % 3 == 2:
            blocks_allowed = [5, 7]
        elif old_move[0] % 3 == 0 and old_move[1] % 3 == 1:
            blocks_allowed = [0, 2]
        elif old_move[0] % 3 == 1 and old_move[1] % 3 == 0:
            blocks_allowed = [0, 6]
        elif old_move[0] % 3 == 2 and old_move[1] % 3 == 1:
            blocks_allowed = [6, 8]
        elif old_move[0] % 3 == 1 and old_move[1] % 3 == 2:
            blocks_allowed = [2, 8]
        elif old_move[0] % 3 == 1 and old_move[1] % 3 == 1:
            blocks_allowed = [4]
        else:
            sys.exit(1)
        final = []
        for i in blocks_allowed:
            if block[i] == '-':
                final.append(i)
        return final

    def get_allowed_moves(self, board, block, old_move):
    	""" Function that gets the allowed moves in a particular state of game
    	:param board:  board input
    	:param block:  list containg status of each block
        :param old_move: previous move
        :return: list of block numbres which are allowed"""
        blocks_allowed = self.get_allowed_blocks(block, old_move)
        return self.get_free_cells(board, blocks_allowed, block)

    def update_block(self, local_board, block_current, block_no, fl):
        local_block = copy.deepcopy(block_current)
        id1 = block_no / 3
        id2 = block_no % 3
        mflg = 0

        flag = 0
        for i in range(id1 * 3, id1 * 3 + 3):
            for j in range(id2 * 3, id2 * 3 + 3):
                if local_board[i][j] == '-':
                    flag = 1

        if local_block[block_no] == '-':
            if local_board[id1 * 3][id2 * 3] == local_board[id1 * 3 + 1][id2 * 3 + 1] and local_board[id1 * 3 + 1][
                                id2 * 3 + 1] == local_board[id1 * 3 + 2][id2 * 3 + 2] and local_board[id1 * 3 + 1][
                                id2 * 3 + 1] != '-' and local_board[id1 * 3 + 1][id2 * 3 + 1] != 'D':
                mflg = 1
            if local_board[id1 * 3 + 2][id2 * 3] == local_board[id1 * 3 + 1][id2 * 3 + 1] and local_board[id1 * 3 + 1][
                                id2 * 3 + 1] == local_board[id1 * 3][id2 * 3 + 2] and local_board[id1 * 3 + 1][
                                id2 * 3 + 1] != '-' and local_board[id1 * 3 + 1][id2 * 3 + 1] != 'D':
                mflg = 1
            if mflg != 1:
                for i in range(id2 * 3, id2 * 3 + 3):
                    if local_board[id1 * 3][i] == local_board[id1 * 3 + 1][i] and local_board[id1 * 3 + 1][i] == \
                            local_board[id1 * 3 + 2][i] and local_board[id1 * 3][i] != '-' and local_board[id1 * 3][
                        i] != 'D':
                        mflg = 1
                        break
            if mflg != 1:
                for i in range(id1 * 3, id1 * 3 + 3):
                    if local_board[i][id2 * 3] == local_board[i][id2 * 3 + 1] and local_board[i][id2 * 3 + 1] == \
                            local_board[i][id2 * 3 + 2] and local_board[i][id2 * 3] != '-' and local_board[i][
                                id2 * 3] != 'D':
                        mflg = 1
                        break
        if flag == 0:
            local_block[block_no] = 'D'
        if mflg == 1:
            local_block[block_no] = fl

        return local_block

    def minimax(self, board, block, old_move, maxnode, player_flag, flag2, depth, alpha, beta, best_row, best_col):
        """
		Applies the minimax algorithm on the state of game
        :param board: board
        :param block: status of blocks
        :param old_move: previous move
        :param maxnode: flag that tells whether it is maxnode or not
        :param player_flag: players flag (x or o)
        :param flag2: opponents flag
        :param depth: depth in tree
        :param alpha: alpha value
        :param beta: beta value
        :param best_row: present best move x-cordinate
        :param best_col: present best move y-cordinate
        :return: three tuple consisting of utlity of block and best moves cordinates
        """

        if depth == self.ply:
            utility = self.get_utility(board, block, player_flag, flag2)
            return (utility, best_row, best_col)
        else:
            moves = self.get_allowed_moves(board, block, old_move)
            # print "Number of moves:",len(moves)
            if len(moves) == 0:
                utility = self.get_utility(board, block, player_flag, flag2)
                utility = round(utility,4)
                self.ply = max(depth, 4)
                return (utility, old_move[0], old_move[1])
            if depth == 0:
                if len(moves) > 10:
                    self.ply = min(self.ply, 4)
            for move in moves:
                # self.isp = 0
                if maxnode:
                    board[move[0]][move[1]] = player_flag
                else:
                    board[move[0]][move[1]] = flag2
                block_no = (move[0] / 3) * 3 + move[1] / 3
                fl = flag2
                if maxnode: fl = player_flag
                temp_block = self.update_block(board, block, block_no, fl)
                if maxnode:

                    util = self.minimax(board, temp_block, move, False, player_flag, flag2, depth + 1, alpha, beta,
                                        best_row,
                                        best_col)
                    utility = round(util[0], 4)
                    if utility > alpha:
                        alpha = utility
                        best_row = move[0]
                        best_col = move[1]
                else:
                    util = self.minimax(board, temp_block, move, True, player_flag, flag2, depth + 1, alpha, beta,
                                        best_row,
                                        best_col)
                    utility = round(util[0], 4)
                    if utility < beta:
                        beta = utility
                        best_row = move[0]
                        best_col = move[1]
                board[move[0]][move[1]] = '-'
                if alpha >= beta:
                    break
            if depth == 0:
                if best_row == '-1' or best_col == '-1':
                    best_row = moves[0][0]
                    best_col = moves[0][1]
            if maxnode:
                return (alpha, best_row, best_col, len(moves))
            else:
                return (beta, best_row, best_col, len(moves))

    def move(self, board, block, old_move, player_flag):
        """
        :param board: is the list of lists that represents the 9x9 grid
        :param block: is a list that represents if a block is won or available to play in
        :param old_move: is a tuple of integers representing co-ordintates of the last move made
        :param flag: is player marker. it can be 'x' or 'o'.
        board[i] can be 'x' or 'o'. block[i] can be 'x' or 'o'
        Chooses a move based on minimax and alphabeta-pruning algorithm and returns it
        :rtype tuple: the co-ordinates in 9X9 board
        """
        self.isp = 0
        if old_move == (-1, -1):
            return (4, 4)
        startt = time.clock()
        if player_flag == 'o':
            flag2 = 'x'
        else:
            flag2 = 'o'
        self.num += 1
        max_ply = 6
        self.cntp = block.count(player_flag)
        self.cnto = block.count(flag2)
        if self.cnto - self.cntp > 1 or self.num > 25 or self.cntp == 2:
            self.ply = max_ply
        temp_board = copy.deepcopy(board)
        temp_block = copy.deepcopy(block)
        next_move = self.minimax(temp_board, temp_block, old_move, True, player_flag, flag2, 0, -100000.0, 100000.0, -1,
                                 -1)
        elapsed = (time.clock() - startt)
        # print "Finally :", next_move, "Took:", elapsed
        return (next_move[1], next_move[2])

    def get_utility(self, board, block, playerFlag, opFlag):
    	"""
    	Function to find and return utility of a block 
    	:param board: is the list of lists that represents the 9x9 grid
        :param block: is a list that represents if a block is won or available to play in
        :param playerFlag: player marker
        :param opFlag: Opponent Marker
    	"""

        util_values = [0 for i in range(9)]
        for i in range(9):
            util_values[i] = self.calc_utility(board, i, playerFlag)
        gain = 0
        lim = 100.0
        for i in range(9):
            util_values[i] /= lim
        for i in range(3):
            p = 0
            cp = 0
            ce = 0
            for j in range(3):
                p += util_values[j * 3 + i]
                if block[j * 3 + i] == playerFlag:
                    cp += 1
                elif block[j * 3 + i] == opFlag:
                    ce += 1
            gain = self.get_factor(p, gain)
            gain = self.get_new(cp, ce, gain)
        for j in range(3):
            p = 0
            cp = 0
            ce = 0
            for i in range(3):
                p += util_values[j * 3 + i]
                if block[j * 3 + i] == playerFlag:
                    cp += 1
                elif block[j * 3 + i] == opFlag:
                    ce += 1
            gain = self.get_factor(p, gain)
            gain = self.get_new(cp, ce, gain)

        p = 0
        cp = 0
        ce = 0
        for i in range(3):
            p += util_values[3 * i + i]
            if block[i * 3 + i] == playerFlag:
                cp += 1
            elif block[i * 3 + i] == opFlag:
                ce += 1
        gain = self.get_factor(p, gain)
        gain = self.get_new(cp, ce, gain)

        p = 0
        cp = 0
        ce = 0
        for i in range(1, 4):
            p += util_values[2 * i]
            if block[i * 2] == playerFlag:
                cp += 1
            elif block[i * 2] == opFlag:
                ce += 1
        gain = self.get_new(cp, ce, gain)
        gain = self.get_factor(p, gain)

        if self.cntp < 2:
            if block[4] == playerFlag:
                gain += 10
            elif block[4] != '-':
                gain -= 10
        cnt1 = block.count(playerFlag)
        cnt2 = block.count(opFlag)
        if self.cntp < cnt1 and cnt2 == self.cnto:
            gain += 50
        elif cnt1 > self.cntp and (cnt1 - self.cntp) < (cnt2 - self.cnto):
            gain -= 20
        elif cnt1 < self.cntp and cnt2 > self.cnto:
            gain -= 50
        return gain

    def calc_utility(self, board, boardno, playerFlag):

        gain = 0
        startx = boardno / 3
        starty = boardno % 3
        starty *= 3
        startx *= 3
        for i in range(startx, startx + 3):
            cp = 0
            ce = 0
            cd = 0
            for j in range(starty, starty + 3):
                if board[i][j] == '-':
                    cd += 1
                elif board[i][j] == playerFlag:
                    cp += 1
                else:
                    ce += 1
            gain = self.calc(cp, ce, gain)

        for j in range(starty, starty + 3):
            cp = 0
            ce = 0
            cd = 0
            for i in range(startx, startx + 3):
                if board[i][j] == '-':
                    cd += 1
                elif board[i][j] == playerFlag:
                    cp += 1
                else:
                    ce += 1
            gain = self.calc(cp, ce, gain)
        cp = 0
        cd = 0
        ce = 0
        for i in range(0, 3):
            if board[startx + i][starty + i] == playerFlag:
                cp += 1
            elif board[startx + i][starty + i] == '-':
                cd += 1
            else:
                ce += 1
        gain = self.calc(cp, ce, gain)
        for i in range(0, 3):
            if board[startx + i][starty + 2 - i] == playerFlag:
                cp += 1
            elif board[startx + i][starty + 2 - i] == '-':
                cd += 1
            else:
                ce += 1
        gain = self.calc(cp, ce, gain)
        return gain

    def calc(self, cx, co, gain):
        if cx == 3:
            gain += 100
        if cx == 2:
            gain += 10
        if cx == 1:
            gain += 1
        if co == 3:
            gain -= 100
        if co == 2:
            gain -= 10
        if co == 1:
            gain -= 1
        return gain

    def get_factor(self, p, gain):
        if p < 1 and p >= -1:
            gain += p
        if p >= 1 and p < 2:
            val = 1
            val += (p - 1) * 9
            gain += val
        if p >= 2 and p < 3:
            val = 10
            val += (p - 1) * 90
            gain += val
        if p >= 3:
            val = 100
            val += (p - 3) * 900
            gain += val
        if p >= -2 and p < -1:
            val = -1
            val -= (abs(p) - 1) * 9
            gain += val
        if p >= -3 and p < -2:
            val = -10
            val -= (abs(p) - 2) * 90
            gain += val
        if p < -3:
            val = -100
            val -= (abs(p) - 3) * 900
            gain += val
        return gain

    def get_new(self, cx, co, gain):
        if cx == 3:
            gain += 1000
        if cx == 2:
            gain += 100
        if cx == 1:
            gain += 10
        if co == 3:
            gain -= 1000
        if co == 2:
            gain -= 100
        if co == 1:
            gain -= 10
        return gain
