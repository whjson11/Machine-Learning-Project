cellSize, columns, rows, trial = 20, 30, 32, 12
initLevel = 1
initScore, initLines, initY, lvlStep, white = 0, 0, 0, 5, 255
colourfav = (228, 204, 200)
pauseMsg = "Paused. Hit P to Resume"
lvlDebuggerMsg = "Debug level"
tetrisFact = []
colours = [
[255, 255, 255],
[255, 255, 255],
[255, 255, 255],
[255, 255, 255],
[255, 255, 255],
[255, 255, 255],
[255, 255, 255],
[255, 255, 255],
[0, 0, 0],
[255, 255, 255],
[255, 255, 255],
[255, 255, 255],
[255, 255, 255],
[0, 0, 0]
]
tetrisShapes = []
tetrisShapes.append([[1, 2, 3, 1]])
tetrisShapes.append([[5, 6, 0], [0, 7, 1]])
tetrisShapes.append([[2, 3], [1, 5]])
tetrisShapes.append([[0, 6, 0], [7, 1, 2]])
tetrisShapes.append([[0 ,3, 1], [5, 6, 0]])
tetrisShapes.append([[7, 1, 2], [0, 0, 3]])
