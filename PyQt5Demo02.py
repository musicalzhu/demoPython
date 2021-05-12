import sys
import time

from PyQt5.QtWidgets import QApplication
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5 import QtCore
from PyQt5.QtCore import QByteArray, QEventLoop, QTimer

import chess
import chess.svg

board = chess.Board()
board.reset_board()

app = QApplication(sys.argv)
svgWidget = QSvgWidget()
svgWidget.setGeometry(400,300,400,400)
svgWidget.show()
board_picture = chess.svg.board(board)

svg_bytes = bytearray(board_picture, encoding='utf-8')
svgWidget.renderer().load(svg_bytes)
svgWidget.update()   
svgWidget.show()

loop = QEventLoop()
QTimer.singleShot(1000, loop.quit)
loop.exec_()

source_cell_index = chess.square(chess.FILE_NAMES.index('a'),chess.RANK_NAMES.index('1'))#example: A1 is cell index = 0 (out of 63)
dest_cell_index = chess.square(chess.FILE_NAMES.index('a'),chess.RANK_NAMES.index('3'))
    
print('source_cell_index:', source_cell_index)
print('dest_cell_index:' , dest_cell_index)

board_picture = chess.svg.board(board,arrows =[(source_cell_index,dest_cell_index)]) #show arrow representing current move

svg_bytes = bytearray(board_picture, encoding='utf-8')
svgWidget.renderer().load(svg_bytes)
svgWidget.update()   
svgWidget.show()

loop = QEventLoop()
QTimer.singleShot(1000, loop.quit)
loop.exec_()

board.push_uci('a2a3')
board_picture = chess.svg.board(board)#show chess board after the move

svg_bytes = bytearray(board_picture, encoding='utf-8')
svgWidget.renderer().load(svg_bytes)
svgWidget.update()   
svgWidget.show()

loop = QEventLoop()
QTimer.singleShot(1000, loop.quit)
loop.exec_()

sys.exit(app.exec_())


