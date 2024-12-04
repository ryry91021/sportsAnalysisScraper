import tkinter as tk
from tkinter import ttk, messagebox

class sportOptionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller

        label=tk.Label(self, text="Choose sport your player is in", font=("Arial", 20))
        label.pack(pady=20)

        #BBall
        basketballButton=tk.Button(self, 
                                   text="Basketball player", 
                                   font=("Arial", 14), 
                                   command= lambda: self.getSportPage("Basketball"))
        basketballButton.pack(pady=10)

        #BaseBall
        baseballButton=tk.Button(self, 
                                   text="Baseball player", 
                                   font=("Arial", 14), 
                                   command= lambda: self.getSportPage("Baseball"))
        baseballButton.pack(pady=10)


        #hockey
        hockeyButton=tk.Button(self, 
                                   text="Hockey player", 
                                   font=("Arial", 14), 
                                   command= lambda: self.getSportPage("Hockey"))
        hockeyButton.pack(pady=10)


    def getSportPage(self, sport):
        if sport=='Basketball':
            return 'basketball-reference.com'
        elif sport=='Baseball':
            return 'baseball-reference.com'
        elif sport=='Hockey':
            return 'hockey-reference.com'
        else:
            return