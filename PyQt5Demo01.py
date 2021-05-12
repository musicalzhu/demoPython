import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5 import QtCore
from PyQt5.QtCore import QByteArray

board_picture = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <svg width="300" height="300" viewBox="0 0 300 300" id="smile" version="1.1">
        <path
            style="fill:#ffaaaa"
            d="M 150,0 A 150,150 0 0 0 0,150 150,150 0 0 0 150,300 150,150 0 0 0 
                300,150 150,150 0 0 0 150,0 Z M 72,65 A 21,29.5 0 0 1 93,94.33 
                21,29.5 0 0 1 72,124 21,29.5 0 0 1 51,94.33 21,29.5 0 0 1 72,65 Z 
                m 156,0 a 21,29.5 0 0 1 21,29.5 21,29.5 0 0 1 -21,29.5 21,29.5 0 0 1 
                -21,-29.5 21,29.5 0 0 1 21,-29.5 z m -158.75,89.5 161.5,0 c 0,44.67 
                -36.125,80.75 -80.75,80.75 -44.67,0 -80.75,-36.125 -80.75,-80.75 z"
        />
    </svg>
    """
def reload_svg():
    print('test001')
    svg_bytes = bytearray(board_picture, encoding='utf-8')
    svgWidget.renderer().load(svg_bytes)
    svgWidget.update()   

app = QApplication(sys.argv)
svgWidget = QSvgWidget()

#reload_svg()

svgWidget.setGeometry(400,300,400,400)
svgWidget.show()

timer = QtCore.QTimer()
timer.start(500)
timer.timeout.connect(reload_svg)

sys.exit(app.exec_())


