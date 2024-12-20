import sys
from PyQt5.QtWidgets import QApplication
from gui import BridgeCostApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BridgeCostApp()
    window.show()
    sys.exit(app.exec_())