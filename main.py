import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MaterialApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MaterialApp()
    window.show()
    sys.exit(app.exec_())