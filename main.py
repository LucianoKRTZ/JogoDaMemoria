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
        self.lastClickedImg = None
        self.correctPair = 0
        self.tries = 0
        self.wins = 0
        self.footer = None

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
        self.rootFooter()

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

    def startGame(self):
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Jogo da Memória")
        self.root.geometry("600x400+0+0")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        self.createGameScreen()
        self.root.mainloop()

    def createGameScreen(self):
        # Placeholder for game screen creation logic
        title = tk.Label(self.root, text="Jogo da Memória", font=("Helvetica", 24), bg="#f0f0f0")
        title.pack(pady=20)

        # Frame principal para organizar as figuras escolhidas
        mainFiguresFrame = tk.Frame(self.root, bg="#f0f0f0")
        mainFiguresFrame.pack(pady=20)

        # Criar pares de figuras (duplicar cada figura)
        self.shuffledFigures = self.tools.shuffleFigures(self.usedFigures)
        
        # Variáveis para controlar as linhas
        buttonsPerRow = 4
        currentRow = None
        buttonCount = 0
        
        # Display the chosen figures
        for idx, figure in enumerate(self.shuffledFigures):
            # Criar nova linha a cada 7 botões
            if buttonCount % buttonsPerRow == 0:
                currentRow = tk.Frame(mainFiguresFrame, bg="#f0f0f0")
                currentRow.pack(pady=5)
        
            figPhotoImg = tk.PhotoImage(file=figure)
            
            # Definir o tamanho desejado (original + 10 pixels)
            zoomedWidth = figPhotoImg.width() + 10
            zoomedHeight = figPhotoImg.height() + 10
            
            # Criar placeholder do tamanho desejado
            placeholder = tk.PhotoImage(width=zoomedWidth, height=zoomedHeight)
            
            figLabel = tk.Button(
                currentRow,  # Usar currentRow em vez de figuresFrame
                image=placeholder,  # Inicialmente com placeholder
                bg="#ffc290",
                borderwidth=1,
                highlightthickness=1,
                relief=tk.RAISED,
                width=zoomedWidth,
                height=zoomedHeight
            )
            # Armazenar a figura original para comparação
            figLabel.figure_path = figure
            
            # Função para mostrar a imagem ao clicar
            def showImage(btn=figLabel, img=figPhotoImg, figurePath=figure):
                btn.config(image=img)
                self.tries += 1
                self.rootFooter()
                if self.lastClickedImg == figurePath:
                    self.setCorrectCombination(figurePath)
                    self.lastClickedImg = None
                elif self.lastClickedImg is not None and \
                     self.lastClickedImg != figurePath:

                    self.hideWrongCombination(figurePath, self.lastClickedImg)
                    self.lastClickedImg = None
                else:
                    self.lastClickedImg = figurePath
            figLabel.config(command=showImage)
            figLabel.image = figPhotoImg  # Prevent garbage collection
            figLabel.placeholder = placeholder  # Prevent garbage collection do placeholder
            figLabel.pack(side=tk.LEFT, padx=5)
            
            buttonCount += 1

        self.rootFooter()

    def setCorrectCombination(self, figurePath):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):  # mainFiguresFrame
                for frame_child in widget.winfo_children():
                    if isinstance(frame_child, tk.Frame):  # currentRow frames
                        for btn in frame_child.winfo_children():
                            if isinstance(btn, tk.Button) and hasattr(btn, "figure_path"):
                                if btn.figure_path == figurePath:
                                    self.correctPair += 1
                                    btn.config(bg="#90ee90", state=tk.DISABLED)  # verde claro
                                    self.checkGameCompletion()

    def hideWrongCombination(self, figurePath, lastClickedImg):
        # Função para esconder as cartas após o delay
        def hideCards():
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame):  # mainFiguresFrame
                    for frame_child in widget.winfo_children():
                        if isinstance(frame_child, tk.Frame):  # currentRow frames
                            for btn in frame_child.winfo_children():
                                if isinstance(btn, tk.Button) and hasattr(btn, "figure_path"):
                                    if btn.figure_path == figurePath or btn.figure_path == lastClickedImg:
                                        btn.config(image=btn.placeholder, bg="#ffc290", state=tk.NORMAL)
        
        # Agendar a função para ser executada após 800ms
        self.root.after(800, hideCards)

    def checkGameCompletion(self):
        if self.correctPair == len(self.usedFigures):
            self.wins += 1
            self.rootFooter()
            completionMessage = tk.Toplevel(self.root)
            completionMessage.title("Parabéns!")
            completionMessage.geometry("400x200")
            completionMessage.resizable(False, False)
            completionMessage.configure(bg="#f0f0f0")
            messageLabel = tk.Label(completionMessage, text="Parabéns!\nVocê completou o jogo!\nAo clicar em fechar o jogo será reiniciado!", font=("Helvetica", 14), bg="#f0f0f0")
            messageLabel.pack(pady=20)
            # Reiniciar o jogo ao fechar a mensagem
            def close_and_restart():
                completionMessage.destroy()
                self.restartGame()
            completionMessage.protocol("WM_DELETE_WINDOW", close_and_restart)
            closeButton = tk.Button(completionMessage, text="Fechar", command=close_and_restart, font=("Helvetica", 14), bg="#f0f0f0")
            closeButton.pack(pady=10)

    def restartGame(self):
        self.usedFigures = []
        self.correctPair = 0
        if self.root:
            self.root.destroy()
        self.startScreen()

    def rootFooter(self):
        if self.footer:
            try:
                self.footer.destroy()
            except Exception as e:
                self.footer = None
        self.footer = tk.Label(self.root, text=f"Tentativas: {self.tries} | Vitórias: {self.wins}", font=("Helvetica", 12), bg="#f0f0f0")
        self.footer.pack(side=tk.BOTTOM, pady=10)
        self.root.update()


if __name__ == "__main__":
    main = Main()
    main.startScreen()