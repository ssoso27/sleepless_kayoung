import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 400

PARENT_WIDTH = WINDOW_WIDTH - 30
PARENT_HEIGHT = WINDOW_HEIGHT - 30

LAYER_HEIGHT = 30

FILE_BOX_WIDTH = 300
FILE_BUTTON_WIDTH = 100
LOG_BOX_HEIGHT = 200


class ChopariteWindow(QMainWindow):
    """Choparite's main window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Choparite")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Set general layout
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)

        # Create components
        self._createInputFileLayer()
        self._createOutputFileLayer()
        self._createGagLayer()
        self._createLogLayer()
        self._createButtonLayer()

    def _createInputFileLayer(self):
        iFileLayout = QHBoxLayout()
        iFileLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        iFileLayout.addWidget(QLabel("파일 (.xlsx)"))

        self.iFileBox = QLineEdit()
        self.iFileBox.setFixedHeight(LAYER_HEIGHT)
        self.iFileBox.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.iFileBox.setReadOnly(True)
        iFileLayout.addWidget(self.iFileBox)

        self.iFileButton = QPushButton("불러오기")
        self.iFileButton.setFixedSize(FILE_BUTTON_WIDTH, LAYER_HEIGHT)
        iFileLayout.addWidget(self.iFileButton)

        self.generalLayout.addLayout(iFileLayout)

    def _createOutputFileLayer(self):
        oFileLayout = QHBoxLayout()
        oFileLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        oFileLayout.addWidget(QLabel("저장위치"))

        self.oFileBox = QLineEdit()
        self.oFileBox.setFixedHeight(LAYER_HEIGHT)
        self.oFileBox.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.oFileBox.setReadOnly(True)
        oFileLayout.addWidget(self.oFileBox)

        self.oFileButton = QPushButton("불러오기")
        self.oFileButton.setFixedSize(FILE_BUTTON_WIDTH, LAYER_HEIGHT)
        oFileLayout.addWidget(self.oFileButton)

        self.generalLayout.addLayout(oFileLayout)

    def _createGagLayer(self):
        gagBox = QLabel("불 꽃 여 자 고 가 영 구 스 리 랑 카 메 라 디 오 징 어 시 장 보 고")
        gagBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.generalLayout.addWidget(gagBox)

    def _createLogLayer(self):
        self.logBox = QTextEdit("실행로그")
        self.logBox.setFixedSize(PARENT_WIDTH, LOG_BOX_HEIGHT)
        self.logBox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.logBox.setReadOnly(True)

        self.generalLayout.addWidget(self.logBox)

    def _createButtonLayer(self):
        self.startButton = QPushButton("분석 시작")
        self.startButton.setFixedSize(PARENT_WIDTH, LAYER_HEIGHT)

        self.generalLayout.addWidget(self.startButton)


    def setLayout1(self):
        layout1 = QHBoxLayout()

        # create widgets
        self.label_fname = QLabel("분석할 파일 (.xlsx): ")
        btn_file = QPushButton("click")
        btn_file.clicked.connect(self.click_btn_file)

        # set widgets
        layout1.addWidget(self.label_fname)
        layout1.addWidget(btn_file)
        return layout1

    def setLayout2(self):
        layout2 = QHBoxLayout()

        # create widgets
        btn_run = QPushButton("RUN")

        # set widgets
        layout2.addWidget(btn_run)
        return layout2


    def click_btn_file(self):
        fname=QFileDialog.getOpenFileName(self, filter="XLSX files (*.xlsx, *.xls)")

        if fname[0]:
            self.filename = fname[0]
            self.label_fname.clear()
            self.label_fname.setText("선택됨: %s" % fname[0].split("/")[-1])
        else:
            print("파일 안 골랐음")
