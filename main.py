from tools import Tools
import tkinter as tk
import random

class Main:
    def __init__(self):
        self.tools = Tools()
        self.root = None
        self.pairs = 4

    def startGame(self):
        self.root = tk.Tk()
        self.root.title("Jogo da Memória")
        self.root.geometry("600x400+0+0")
        self.root.resizable(False, False)
        self.createInitialMenu()
        self.root.mainloop()

    def createInitialMenu(self):
        self.root.configure(bg="#f0f0f0")
        title = tk.Label(self.root, text="Jogo da Memória", font=("Helvetica", 24), bg="#f0f0f0")
        title.pack(pady=20)

        subTitle = tk.Label(self.root, text="Escolha com quantos pares de figuras quer jogar", font=("Helvetica", 16), bg="#f0f0f0")
        subTitle.pack(pady=10)

        # Frame para organizar os botões e o número na mesma linha
        controlFrame = tk.Frame(self.root, bg="#f0f0f0")
        controlFrame.pack(pady=20)

        chevronLeftImg = tk.PhotoImage(file="assets/square-chevron-left.png")
        self.lessBtn = tk.Button(controlFrame, image=chevronLeftImg, command=self.decreasePairs, font=("Helvetica", 14), bg="#f0f0f0", relief=tk.FLAT, borderwidth=0, highlightthickness=0)
        self.lessBtn.image = chevronLeftImg  # Prevent garbage collection
        self.lessBtn.pack(side=tk.LEFT, padx=20)

        self.pairsLabel = tk.Label(controlFrame, text=self.pairs, font=("Helvetica", 18), bg="#f0f0f0")
        self.pairsLabel.pack(side=tk.LEFT, padx=30)

        chevronRightImg = tk.PhotoImage(file="assets/square-chevron-right.png")
        self.moreBtn = tk.Button(controlFrame, image=chevronRightImg, command=self.increasePairs, font=("Helvetica", 14), bg="#f0f0f0", relief=tk.FLAT, borderwidth=0, highlightthickness=0)
        self.moreBtn.image = chevronRightImg  # Prevent garbage collection
        self.moreBtn.pack(side=tk.LEFT, padx=20)

    def decreasePairs(self):
        self.pairs -= 1
        if self.pairs <= 2:
            self.lessBtn.config(state=tk.DISABLED)
            self.pairs = 2
        elif self.lessBtn['state'] == tk.DISABLED:
            self.lessBtn.config(state=tk.NORMAL)

        elif self.moreBtn['state'] == tk.DISABLED:
            self.moreBtn.config(state=tk.NORMAL)

        self.updatePairsLabel()

    def increasePairs(self):
        self.pairs += 1
        if self.pairs >= 5:
            self.moreBtn.config(state=tk.DISABLED)
            self.pairs = 5
        elif self.moreBtn['state'] == tk.DISABLED:
            self.moreBtn.config(state=tk.NORMAL)
        
        if self.lessBtn['state'] == tk.DISABLED:
            self.lessBtn.config(state=tk.NORMAL)

        self.updatePairsLabel()

    def updatePairsLabel(self):
        self.pairsLabel.config(text=self.pairs)

if __name__ == "__main__":
    main = Main()
    main.startGame()