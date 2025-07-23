from tools import Tools
import tkinter as tk
import random
import os

class Main:
    def __init__(self):
        self.tools = Tools()
        self.root = None
        self.pairs = 4
        self.maxPairs = len([i for i in os.listdir(self.tools.assetsPath) if i.lower().startswith("fig-")])
        self.usedFigures = []
        self.figsMenuFrame = None

    def startScreen(self):
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

        # Frame para organizar as figuras que serao jogadas
        self.figsMenuFrame = tk.Frame(self.root, bg="#f0f0f0")
        self.figsMenuFrame.pack(pady=20)

        chevronLeftImg = tk.PhotoImage(file="assets/_square-chevron-left.png")
        self.lessBtn = tk.Button(controlFrame, image=chevronLeftImg, command=self.decreasePairs, font=("Helvetica", 14), bg="#f0f0f0", relief=tk.FLAT, borderwidth=0, highlightthickness=0)
        self.lessBtn.image = chevronLeftImg  # Prevent garbage collection
        self.lessBtn.pack(side=tk.LEFT, padx=20)

        self.pairsLabel = tk.Label(controlFrame, text=self.pairs, font=("Helvetica", 18), bg="#f0f0f0")
        self.pairsLabel.pack(side=tk.LEFT, padx=30)

        chevronRightImg = tk.PhotoImage(file="assets/_square-chevron-right.png")
        self.moreBtn = tk.Button(controlFrame, image=chevronRightImg, command=self.increasePairs, font=("Helvetica", 14), bg="#f0f0f0", relief=tk.FLAT, borderwidth=0, highlightthickness=0)
        self.moreBtn.image = chevronRightImg  # Prevent garbage collection
        self.moreBtn.pack(side=tk.LEFT, padx=20)

        # Inicializar figuras baseadas no valor inicial de pairs
        self.initializeFigures()

        self.startGameButton = tk.Button(self.root, text="Iniciar Jogo", command=self.startGame, font=("Helvetica", 16), bg="#f0f0f0")
        self.startGameButton.pack(pady=20)

    def decreasePairs(self):
        self.pairs -= 1
        if self.pairs <= 2:
            self.lessBtn.config(state=tk.DISABLED)
            self.pairs = 2
        elif self.lessBtn['state'] == tk.DISABLED:
            self.lessBtn.config(state=tk.NORMAL)

        if self.moreBtn['state'] == tk.DISABLED:
            self.moreBtn.config(state=tk.NORMAL)

        # Remover figura se necessário
        if len(self.usedFigures) > self.pairs:
            self.usedFigures.pop()

        self.updatePairsLabel()
        self.addFigureToMenu()

    def increasePairs(self):
        self.pairs += 1
        if self.pairs >= self.maxPairs:
            self.moreBtn.config(state=tk.DISABLED)
            self.pairs = self.maxPairs        
        
        if self.lessBtn['state'] == tk.DISABLED:
            self.lessBtn.config(state=tk.NORMAL)

        # Adicionar figura se necessário
        if len(self.usedFigures) < self.pairs:
            newFigure = self.tools.chooseFigure(self.usedFigures)
            self.usedFigures.append(newFigure)

        self.updatePairsLabel()
        self.addFigureToMenu()

    def updatePairsLabel(self):
        self.pairsLabel.config(text=self.pairs)

    def initializeFigures(self):
        # Inicializar com o número correto de figuras baseado em self.pairs
        while len(self.usedFigures) < self.pairs:
            newFigure = self.tools.chooseFigure(self.usedFigures)
            self.usedFigures.append(newFigure)
        self.addFigureToMenu()

    def addFigureToMenu(self):
        print(f"New figure added: {self.usedFigures[-1]}")
        # Limpar figuras existentes antes de adicionar todas novamente
        for widget in self.figsMenuFrame.winfo_children():
            widget.destroy()

        # Criar dois frames para as linhas de figuras
        topRow = tk.Frame(self.figsMenuFrame, bg="#f0f0f0")
        bottomRow = tk.Frame(self.figsMenuFrame, bg="#f0f0f0")
        topRow.pack()
        bottomRow.pack()

        # Adicionar figuras: até 5 na primeira linha, o resto na segunda
        for idx, figure in enumerate(self.usedFigures):
            figPhotoImg = tk.PhotoImage(file=figure)
            figLabel = tk.Label(
                topRow if idx < 5 else bottomRow,
                image=figPhotoImg,
                bg="#f0f0f0"
            )
            figLabel.image = figPhotoImg  # Prevent garbage collection
            figLabel.pack(side=tk.LEFT, padx=5)


if __name__ == "__main__":
    main = Main()
    main.startScreen()