import sys
import os
from PyQt5.QtWidgets import QApplication

# Add the parent directory to Python path to make package imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
