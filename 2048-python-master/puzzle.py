import random
from tkinter import Frame, Label, CENTER

import logic
import constants as c


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)
        self.path = "./images/data.txt"
        self.reward = 0.5
        self.punish = -0.01
        self.max = 0
        self.num = 0
        self.lastState = []
        self.flagBreak = 0

        # self.gamelogic = gamelogic
        self.commands = {c.KEY_UP: logic.up, c.KEY_DOWN: logic.down,
                         c.KEY_LEFT: logic.left, c.KEY_RIGHT: logic.right,
                         c.KEY_UP_ALT: logic.up, c.KEY_DOWN_ALT: logic.down,
                         c.KEY_LEFT_ALT: logic.left, c.KEY_RIGHT_ALT: logic.right,
                         c.KEY_H: logic.left, c.KEY_L: logic.right,
                         c.KEY_K: logic.up, c.KEY_J: logic.down}
        
        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE / c.GRID_LEN,
                             height=c.SIZE / c.GRID_LEN)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def gen(self):
        return random.randint(0, c.GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = list()
        self.matrix = logic.add_two(self.matrix)
        self.matrix = logic.add_two(self.matrix)

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(
                        text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(
                        new_number), bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def writeToFile(self, key):
        liste = []
        if (self.flagBreak == 0):
            if (self.lastState != []):
                liste.append(self.num)
                self.num += 1
                liste.append(self.lastState)
                liste.append(self.matrix)
                maximilian = 0
                maximilius = 0
                for x in self.matrix:
                    for y in x:
                        if (y == 9999999):
                            self.flagBreak = 1
                            self.reward = -1
                for x in self.lastState:
                    if(maximilian < max(x)):
                        maximilian = max(x)
                for x in self.matrix:
                    if(maximilius < max(x)):
                        maximilius = max(x)
                if(maximilius > maximilian):
                    liste.append(self.reward)
                else:
                    liste.append(self.punish)
                liste.append(key)
            else:
                liste = ["Nummer, Matrix_Alt, Matrix_Neu, reward, PressedKey"]

            f = open(self.path, "a")
            f.write(str(liste) + "\n")
            f.close()
            self.lastState = self.matrix

    def key_down(self, event):
        key = repr(event.char)
        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
        elif key in self.commands:
            self.matrix, done = self.commands[repr(event.char)](self.matrix)
            if done:
                self.matrix = logic.add_two(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                done = False
                if logic.game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                if logic.game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.matrix[0][0] = 9999999
        self.writeToFile(key)

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2


gamegrid = GameGrid()
