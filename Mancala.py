import socket
import numpy as np
import time
from multiprocessing.pool import ThreadPool
import copy


class Batu():
    def __init__(self, player_turn, board):
        self.player = player_turn
        self.board = board
        self.extra_turn = False

    def findValidMoves(self):
        available = []
        board = self.board
        if self.player == 1:
            for i in range(6):
                if board[i] != 0:
                    available.append(i + 1)
        elif self.player == 2:
            for i in range(7, 13):
                if board[i] != 0:
                    available.append(i - 6)
        return available


    def isFinish(self):
        if sum([self.board[i] for i in range(6)]) == 0 or sum([self.board[i] for i in range(7,13)]) == 0:
            return True
        else:
            return False


    def makeMove(self, move):
        self.extra_turn = False
        turn = self.player
        if move == 0 or move == 7:
            print("MOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVE")
            print(move)
            print("MOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVEMOVE")

        change_player = True
        if self.player == -1:
            return board
        boardc = self.board.copy()

        if turn == 1:
            last = 0
            hand = boardc[move]
            boardc[move] = 0
            idx = move +1
            skip = 0
            for i in range(hand):
                val = (move + i + skip) % 14
                if val == 13:
                    skip += 1
                    val = (move + i + skip) % 14
                boardc[val] += 1
                last = val
            if last == 6:
                self.player = 1
                change_player = False

            if 0 <= last < 6 and boardc[last] == 1:
                boardc[6] += (1 + boardc[12 - last])
                boardc[last] = 0
                boardc[12 - last] = 0
                res_board = boardc.copy()
            else:
                res_board = boardc.copy()

            if change_player:
                self.player = 2
            self.board = res_board.copy()
        if turn == 2:
            last = 0
            hand = boardc[move + 6]
            boardc[move + 6] = 0
            skip = 0
            for i in range(hand):
                val = (move + i + skip + 7) % 14
                if val == 6:
                    skip += 1
                    val = (move + i + skip + 7) % 14

                boardc[val] += 1
                last = val
            if last == 13:
                self.player = 1
                change_player = False
                self.extra_turn = True
            if 7 <= last < 13 and boardc[last] == 1:
                boardc[13] += (1 + boardc[12 - last])
                boardc[last] = 0
                boardc[12 - last] = 0
                res_board = boardc.copy()
            else:
                res_board = boardc.copy()
            if change_player:
                self.player = 2
            self.board =  res_board

    def win_diff(self, turn, borad):
        if turn == 1:
            return board[6] - board[13]
        else:
            return board[13] - board[6]

    def empty_count(self,turn, board):

        if turn == 1:
            l = sum([1 for i in range(6) if i == 0])
        else:
            l = sum([1 for i in range(7, 13) if i == 0])
        return l


    def turn_changer(self,turn):
        if turn == 1:
            return 2
        return 1

    def is_win(self, turn, borad):
        if self.stones_on_side(turn, board) == 0 or self.stones_on_side(self.turn_changer(turn), borad) == 0:
            if turn == 1 and board[6] > board[13]:
                return True
            elif turn == 2 and board[13] > board[6]:
                return True
        return False

    def extra_turn_num(self,turn, board):
        num = 0
        if turn == 1:
            for i in range(6):
                if i + board[i] == 6:
                    num += 1
        else:
            for i in range(7, 12):
                if i + board[i] == 13:
                    num += 1
        return num

    def last_drop(self, turn, board):
        sum = 0
        flag = False
        if turn == 1:
            for i in range(6):
                if (i + board[i]) % 12 < 6 and board[12 - (i + board[i])] != 0:
                    for j in range(6):
                        if board[j + 7] == abs((12 - (i + board[i])) - (j + 7)):
                            flag = True
                    if flag:
                        sum += board[12 - (i + board[i])] / 4
                    else:
                        sum += board[12 - (i + board[i])] / 2

        else:
            for i in range(6):
                if 6 < (i + board[i + 7]) % 12 < 13 and board[12 - (i + board[i + 7])] != 0:
                    for j in range(6):
                        if board[j] == abs((12 - (i + board[i + 7])) - (j)):
                            flag = True
                    if flag:
                        sum += board[12 - (i + board[i + 7])] / 4
                    else:
                        sum += board[12 - (i + board[i + 7])] / 2
        return sum

    def mancala_stones(self,turn, board):
        if turn == 1:
            return board[6]
        return board[13]

    def utility(self, state):
        turn = self.player
        board = self.board.copy()
        weights = [1, 3, 5]#this is the weight vector created by hand
        util_array = [] #this is utility array that we collect our utility values

        res = 0 # this is result parameter and summation after multiplication with weights
        stones = 0
        for i in range(7, 13):
            #This for loop counts the stones in our side
            stones += state.board[i]
        util_array.append(stones)#we are adding number of stones in the array
        util_array.append(state.board[13]) #we are adding number of stones in our mancala pit to array

        if self.extra_turn:#we are cheecking if we have any extra turn in this state
            util_array.append(1)
        else:
            util_array.append(0)
        
        res = 0
        for i in range(3):# we are multiplying every utility value with its weight and summing them in res parameter
            res += weights[i]*util_array[i]
        return res

        """util_array.append(stones+score)
        # util_array.append(self.stones_on_side(self.turn_changer(turn), board))
        # win difference
        util_array.append(board[13] - board[6])
        #self empty pit count
        util_array.append(sum([1 for i in range(7, 13) if i == 0]))
        #iswin
        if board[13] > board[6] and (sum([i for i in range(7,13) if self.board[i] == 0]) == 0 or sum([i for i in range(6) if self.board[i] == 0]) == 0):
            util_array.append(1)
        else:
            util_array.append(0)
        #util_array.append(self.is_win(self.turn_changer(turn), board))
        #util_array.append(self.last_drop(turn, board))
        #util_array.append(self.mancala_stones(turn, board) - self.mancala_stones(self.turn, prev_board))
        #l = sum([1 for i in range(7, 13) if i == 0])

        total = 0
        for i in range(4):
            total += weights[i]*util_array[i]
        return total"""


def chose_best(state):
    avail = state.findValidMoves()
    max_val = -9999
    best_move = None
    for move in avail:
        new_state = copy.deepcopy(state)
        new_state.makeMove(move)
        val = minimax(new_state, 2, -9999, 9999)
        if val > max_val:
            max_val = val
            best_move = move
    return best_move


def minimax(state, depth, alpha, beta):
    min_Eval = 9999
    max_Eval = -9999
    avail = state.findValidMoves()
    if state.isFinish() or depth == 0:
        return state.utility(state)

    if state.player == 1:
        for v in avail:
            new_board = copy.deepcopy(state)
            new_board.makeMove(v)
            evaluate = minimax(new_board, depth - 1, alpha, beta)
            maxEval = max(max_Eval, evaluate)
            alpha = max(alpha, evaluate)
            if beta <= alpha:
                break
        return maxEval
    else:
        for v in avail:
            new_board = copy.deepcopy(state)
            new_board.makeMove(v)
            evaluate = minimax(new_board, depth - 1, alpha, beta)
            minEval = min(min_Eval, evaluate)
            beta = min(beta, evaluate)
            if beta <= alpha:
                break
        return minEval

def receive(socket):
    msg = ''.encode()  # type: str

    try:
        data = socket.recv(1024)  # type: object
        msg += data
    except:
        pass
    return msg.decode()


def send(socket, msg):
    socket.sendall(repr(msg).encode('utf-8'))



playerName = 'Batu'
host = '127.0.0.1'
port = 30000  # Reserve a port for your service.
s = socket.socket()  # Create a socket object
pool = ThreadPool(processes=1)
gameEnd = False
MAX_RESPONSE_TIME = 5

print('The player: ' + playerName + ' starts!')
s.connect((host, port))
print('The player: ' + playerName + ' connected!')

while not gameEnd:
    asyncResult = pool.apply_async(receive, (s,))
    startTime = time.time()
    currentTime = 0
    received = 0
    data = []
    while received == 0 and currentTime < MAX_RESPONSE_TIME:
        if asyncResult.ready():
            data = asyncResult.get()
            received = 1
        currentTime = time.time() - startTime

    if received == 0:
        print('No response in ' + str(MAX_RESPONSE_TIME) + ' sec')
        gameEnd = 1

    if data == 'N':
        send(s, playerName)

    if data == 'E':
        gameEnd = 1

    if len(data) > 1:

        # Read the board and player turn
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        playerTurn = int(data[0])
        i = 0
        j = 1
        while i <= 13:
            board[i] = int(data[j]) * 10 + int(data[j + 1])
            i += 1
            j += 2
        # Using your intelligent bot, assign a move to "move"
        #
        # example: move = '1';  Possible moves from '1' to '6' if the game's rules allows those moves.
        # TODO: Change this
        ################
        state = Batu(playerTurn, board)
        move = chose_best(state)
        ################
        send(s, move)
