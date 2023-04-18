"""
Copyright (C) 2023. YangSohee all rights reserved.
Author: Yang Sohee <ssoyapdev@gmail.com>

Choparite 컨트롤러 (Controller)
"""
from PyQt5.QtWidgets import QFileDialog

class ChopariteController:
    def __init__(self, service, view):
        self._service = service
        self._view = view
        self._connectSignalsAndSlots()
        self._service.set_logger(self._view.log)

    def _loadFile(self):
        fname = QFileDialog.getOpenFileName(self._view, filter="XLSX files (*.xlsx *.xls)")
        if not fname[0]:
            self._view.log("파일을 불러오는데 실패하였습니다.")
            return
        filename = self._service.load_data(fname[0])
        self._view.setIFileText(filename)

    def _setOutputDir(self, dirpath):
        dirpath = self._service.set_output_dir(dirpath)
        self._view.setOFileText(dirpath)

    def _analyze(self):
        ifile = self._view.getIFileText()
        if not ifile.strip():
            self._view.log("Please input file.")
            return
        self._service.check_sleep()
        self._view.toggleButton()

    def _save(self):
        fname = QFileDialog.getSaveFileName(self._view,
                    caption="초파리떼 결과 저장",
                    filter="XLSX files (*.xlsx *.xls)",
                    directory=self._service.make_filename(),
                )
        if not fname[0]:
            self._view.log("분석 결과 저장에 실패하였습니다.")
            return
        output = self._service.save_to_excel(output_filename=fname[0])
        self._view.log(f"Save success: {output}")

    def _connectSignalsAndSlots(self):
        self._view.iFileButton.clicked.connect(self._loadFile)
        self._view.startButton.clicked.connect(self._analyze)
        self._view.saveButton.clicked.connect(self._save)