import math

class table():
    def __init__(self, filename):
        #1-spy-1
        #2-scout-8
        #3-miner-5
        #4-seargent-4
        #5-lieutenant-4
        #6-captain-4
        #7-major-3
        #8-colonel-2
        #9-general-1
        #10-marshal-1
        #11-Bomb-6
        #12-Flag-1
        #13-inaccessible-x
        #14-hidden enemy-x
        self.game_pieces = {
            1:1,
            2:8,
            3:5,
            4:4,
            5:4,
            6:4,
            7:3,
            8:2,
            9:1,
            10:1,
            11:6,
            12:1,
            13:99,
            14:99,
        }

        self.filename = filename
        self.player1_pieces = {}
        self.player2_pieces = {}
        self.positions = []
        self.width = 0
        self.height = 0
        self.hidden_p1_pieces = 0
        self.hidden_p2_pieces = 0
        self.h1p = 0
        self.h2p = 0
        self.ammount_of_spaces_line = 0
        self.coordinates = {}
        self.board = {}

        #Read contents of the table
        with open(filename) as f:
            self.contents = f.read()
        self.contents = self.contents.splitlines()

        #Remove flair from code
        for i in self.contents:
            for e in i:
                if e == "-":
                    self.contents.remove(i)
                    break
        self.contents = [i.replace("|", "") for i in self.contents]

        #Set width and height of board
        self.width = max(len(lines) for lines in self.contents)
        self.height = len(self.contents)

        #Set coordinates
        lines = []
        for temp_lines in range(self.width):
            temp_lines += 1
            lines.append(temp_lines)
        for temp_collums in range(self.height):
            temp_collums += 1
            self.coordinates.update({temp_collums:lines})

        
    # function to return key for any value
    def get_key(val, dictionary):
        for key, value in dictionary.items():
            if val == value:
                return key
    
        return "key doesn't exist"


    #Place pieces on game board
    #Pieces
    def place_piece(self, player, piece, line, collum):
        self.ammount_of_spaces_line = list(self.coordinates.values())
        self.ammount_of_spaces_line = self.ammount_of_spaces_line[0]
        ammount_pieces_played = 0
        dup_error = 0
        get_hidden = 0
        if 0 < collum <= max(self.coordinates.keys()):  
            if 0 < line <= max(self.ammount_of_spaces_line):
                for board_piece, board_coor in self.board.items():
                    if (board_coor[1], board_coor[0]) == (collum, line):
                        dup_error = 1
                if dup_error:
                    return False
                else:
                    if player == 0:
                        for piece_in_board in self.player1_pieces:
                            if math.floor(piece_in_board) == math.floor(piece):
                                ammount_pieces_played += 1
                    elif player == 1:
                        for piece_in_board in self.player2_pieces:
                            if math.floor(piece_in_board) == math.floor(piece):
                                ammount_pieces_played += 1
                    if self.game_pieces[math.floor(piece)] > ammount_pieces_played:

                        self.board.update({piece:[line,collum]})
                        if player == 0:
                            self.player1_pieces.update({piece:[line,collum]})
                            for p2_piece in self.player2_pieces:
                                if math.floor(p2_piece) == 14:
                                    get_hidden = 1
                                    break
                            if get_hidden == 1:
                                self.h1p += 0.01
                            self.player2_pieces.update({14.00 + self.h1p:[line,collum]})
                        elif player == 1:
                            self.player2_pieces.update({piece:[line,collum]})
                            for p1_piece in self.player1_pieces:
                                if math.floor(p1_piece) == 14:
                                    get_hidden = 1
                                    break
                            if get_hidden == 1:
                                self.h2p += 0.01
                            self.player1_pieces.update({14.00 + self.h2p:[line,collum]})
                        elif player == 2:
                            self.player1_pieces.update({piece:[line,collum]})
                            self.player2_pieces.update({piece:[line,collum]})
                        return True
                    else:
                        return False
            else:
                return False
        else:
            return False

    #Scenario
    def create_scenario(self):
        new_piece_13 = 0
        line_number = 0
        for line in self.contents:
            space_number = 0
            line_number += 1
            for space in line:
                space_number += 1
                if space == "x":
                    place_piece(self, 2, 13.00 + new_piece_13, line_number, space_number)
                    new_piece_13 += 0.01

    
    #Move pieces
    def ez_move(self, player, piece, ammount, direction):
        move = []
        obstruction = 1
        conflict = 0
        conflict_pc = 0
        conflict_pc_p1 = 0
        hidden_conf_pc_p1 = 0
        conflict_pc_p2 = 0
        hidden_conf_pc_p2 = 0
        if piece != 2:
            ammount = 1
        #up
        if direction == 0:
            temp = self.board[piece]
            move = [temp[0] - ammount, temp[1]]
        #down
        elif direction == 1:
            temp = self.board[piece]
            move = [temp[0] + ammount, temp[1]]
        #left
        elif direction == 2:
            temp = self.board[piece]
            move = [temp[0], temp[1] - ammount]
        #right
        elif direction == 3:
            temp = self.board[piece]
            move = [temp[0], temp[1] + ammount]

        #check for obstruction/conflict in path
        if player == 0:
            for pc, coor in self.player1_pieces.items():
                if (math.floor(pc) == 13) and (0 < move[0] < max(self.coordinates.keys()) and (0 < move[1] < max(self.ammount_of_spaces_line))):
                    #not obstructed
                    obstruction = 1
                if (math.floor(pc) == 14) and (0 < move[0] < max(self.coordinates.keys()) and (0 < move[1] < max(self.ammount_of_spaces_line))):
                    #conflict against hidden piece aka: piece number 14
                    conflict = 1
                    conflict_pc_p1 = piece
                    conflict_pc = conflict_pc_p2 = get_key(coor, self.player2_pieces)
                    hidden_conf_pc_p1 = get_key(coor, self.player1_pieces)
                    hidden_conf_pc_p2 = get_key(self.player1_pieces[piece], self.player2_pieces)
            
            if not obstruction:
                self.player1_pieces[piece] = move
                self.player2_pieces[get_key(temp, self.player2_pieces)] = move

        elif player == 1:
            for pc, coor in self.player2_pieces.items():
                if (math.floor(pc) == 13) and (0 < move[0] < max(self.coordinates.keys()) and (0 < move[1] < max(self.ammount_of_spaces_line))):
                    #obstructed
                    obstruction = 1
                if (math.floor(pc) == 14) and (0 < move[0] < max(self.coordinates.keys()) and (0 < move[1] < max(self.ammount_of_spaces_line))):
                    #conflict against hidden piece aka: piece number 14
                    conflict = 1
                    conflict_pc_p2 = piece
                    conflict_pc = conflict_pc_p1 = get_key(coor, self.player1_pieces)
                    hidden_conf_pc_p2 = get_key(coor, self.player2_pieces)
                    hidden_conf_pc_p1 = get_key(self.player2_pieces[piece], self.player1_pieces)

            if not obstruction:
                self.player2_pieces[piece] = move
                self.player1_pieces[get_key(temp, self.player1_pieces)] = move

                
        #conflict solve
        if conflict:
            print(conflict_pc_p2, hidden_conf_pc_p1)
            if math.floor(piece) > math.floor(conflict_pc):
                self.board.pop(conflict_pc)
                if player == 0:
                    self.player1_pieces.pop(hidden_conf_pc_p1)
                    self.player2_pieces.pop(conflict_pc_p2)
                if player == 1:
                    self.player2_pieces.pop(hidden_conf_pc_p2)
                    self.player1_pieces.pop(conflict_pc_p1)
            elif math.floor(piece) == math.floor(conflict_pc):
                self.board.pop(conflict_pc_p1)
                self.board.pop(conflict_pc_p2)
                self.player2_pieces.pop(conflict_pc_p2)
                self.player1_pieces.pop(conflict_pc_p1)
                self.player2_pieces.pop(hidden_conf_pc_p2)
                self.player1_pieces.pop(hidden_conf_pc_p1)
            elif math.floor(piece) < math.floor(conflict_pc):
                if player == 0:
                    self.board.pop(conflict_pc_p1)
                    self.player1_pieces.pop(conflict_pc_p1)
                    self.player2_pieces.pop(hidden_conf_pc_p2)
                if player == 1:
                    self.board.pop(conflict_pc_p2)
                    self.player2_pieces.pop(conflict_pc_p2)
                    self.player1_pieces.pop(hidden_conf_pc_p1)
        elif obstruction:
            return False


    def move_piece_up(self, player, piece, ammount):
        return ez_move(player, piece, ammount, 0)
    def move_piece_down(self, player, piece, ammount):
        return ez_move(player, piece, ammount, 1)
    def move_piece_left(self, player, piece, ammount):
        return ez_move(player, piece, ammount, 2)
    def move_piece_right(self, player, piece, ammount):
        return ez_move(player, piece, ammount, 3)
        


"""
a = table('C:/Users/bdavi/OneDrive/Área de Trabalho/stratego/board.txt')
a.place_piece(0, 3.11, 1, 1)
a.place_piece(1, 3.01, 1, 2)

print("player1 before move:")
print(a.player1_pieces)
print("\nplayer2 before move:")
print(a.player2_pieces)
print("\nboard before move:")
print(a.board)

move_piece_left(1, 3.01, 1)

#print(len(self.board))
print("\nplayer1 after move:")
print(self.player1_pieces)
print("\nplayer2 after move:")
print(self.player2_pieces)
print("\nboard after move:")
print(self.board)
"""