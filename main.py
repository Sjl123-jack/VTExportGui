import sys
from PyQt5.QtWidgets import *
from TrayApp import TrayApp


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tray_app = TrayApp(app.processEvents)
    tray_app.quitAction.triggered.connect(app.quit)
    app.setQuitOnLastWindowClosed(False)
    sys.exit(app.exec_())
