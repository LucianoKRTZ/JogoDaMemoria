import os
import random

class Tools:
    def __init__(self):
        self.assetsPath = "assets/"

    def chooseFigure(self, usedFigures):
        allFigures = os.listdir(self.assetsPath)

        availableFigures = [fig for fig in allFigures if os.path.join(self.assetsPath, fig) not in usedFigures and fig.startswith("fig-")]
        if availableFigures:
            return os.path.join(self.assetsPath, random.choice(availableFigures))