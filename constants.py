cellSize, columns, rows, trial = 20, 30, 32, 12
initLevel = 1
initScore, initLines, initY, lvlStep, white = 0, 0, 0, 5, 255
colourfav = (228, 204, 200)
pauseMsg = "Paused. Hit P to Resume"
lvlDebuggerMsg = "Debug level"
tetrisFact = []
colours = [
[86, 108, 48],
[0, 240, 240],
[149, 160, 217],
[0, 0, 240],
[36, 34, 37],
[240, 160, 2],
[254, 86, 85],
[240, 240, 0],
[55, 69, 79],
[0, 240, 0],
[121, 107, 244],
[160, 0, 240],
[149, 160, 217],
[36, 34, 36]
]
tetrisShapes = []
tetrisShapes.append([[1, 2, 3, 1]])
tetrisShapes.append([[5, 6, 0], [0, 7, 1]])
tetrisShapes.append([[2, 3], [1, 5]])
tetrisShapes.append([[0, 6, 0], [7, 1, 2]])
tetrisShapes.append([[0 ,3, 1], [5, 6, 0]])
tetrisShapes.append([[7, 1, 2], [0, 0, 3]])
