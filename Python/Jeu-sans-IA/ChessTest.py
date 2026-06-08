import chess
import chess.svg
import random
import tkinter as tk
from tkinter import *

board = chess.Board()
player1 = chess.BLACK
aiPlayer = chess.WHITE
root = tk.Tk()
menu = tk.Menu(root)
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

def createBoard() :
    table = Canvas(root, width=400, height=400, background="black")
    print(table.winfo_width())
    x_center = (width/2) - table.winfo_width()
    y_center = (height/2) - table.winfo_height()
    table.place(x=x_center, y=y_center)

def defineWhite() :
    if random.randint(0, 10) <= 5 :
        player1 = chess.WHITE
        aiPlayer = chess.BLACK

def gui() :
    # Window Config
    root.title("Chess application")
    root.config(menu=menu)

    # New Game
    newGameMenu = tk.Menu(menu)
    menu.add_cascade(label="Nouvelle Partie", menu=newGameMenu)

    # Options
    optionMenu = tk.Menu(menu)
    menu.add_cascade(label="Options", menu=optionMenu)
    optionMenu.add_command(label="Time")
    optionMenu.add_command(label="Level")
    optionMenu.add_command(label="Color")
    optionMenu.add_separator()
    optionMenu.add_command(label="Preferences")
    optionMenu.add_command(label="Theme")

    # Help
    helpMenu = tk.Menu(menu)
    menu.add_cascade(label="Aide", menu=helpMenu)

    #Chess Board
    createBoard()
    root.mainloop()

gui()