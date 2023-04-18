import sys
from PyQt5.QtWidgets import QApplication
from choparite_window import ChopariteWindow

def main():
    """Choparite's main function"""
    app = QApplication([])
    window = ChopariteWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
