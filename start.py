import sys
from PyQt5.QtWidgets import QApplication
from choparite_controller import ChopariteController
from choparite_service import ChopariteService
from choparite_window import ChopariteWindow

def main():
    """Choparite's main function"""
    app = QApplication(sys.argv)
    window = ChopariteWindow()
    window.show()
    service = ChopariteService()
    controller = ChopariteController(service=service, view=window)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
