import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLineEdit, QLabel
from PyQt5.uic import loadUi
from fileMapper import FileMapper


def main():

    appInput = {
        "root_dir": "UNDEFINED",
        "json_path": "UNDEFINED",
        "ext_omits": [],
        "generated": False
    }


    class MainWindow(QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()
            loadUi("mainWindow.ui", self)

            # Widgets
            self.rootLineEdit = self.findChild(QLineEdit, "rootDirLineEdit")
            self.rootButton = self.findChild(QPushButton, "rootDirButton")

            self.jsonPathLineEdit = self.findChild(QLineEdit, "jsonPathLineEdit")
            self.jsonPathButton = self.findChild(QPushButton, "jsonPathButton")

            self.extLineEdit = self.findChild(QLineEdit, "extLineEdit")
            self.extButton = self.findChild(QPushButton, "extButton")
            self.extOmitLabel = self.findChild(QLabel, "extOmitLabel")

            self.generateButton = self.findChild(QPushButton, "GenerateButton")
            self.statusLabel = self.findChild(QLabel, "statusLabel")
            self.outPutDirButton = self.findChild(QPushButton, "outputDirButton")
            self.outputButton = self.findChild(QPushButton, "outputFilePath")

            # Widget Functionality
            self.rootButton.clicked.connect(self.DefineRoot)
            self.jsonPathButton.clicked.connect(self.JsonPath)
            self.extButton.clicked.connect(self.ExtOmits)
            self.generateButton.clicked.connect(self.Generate)
            self.outPutDirButton.clicked.connect(self.GoToOutPutDir)
            self.outputButton.clicked.connect(self.GoToFile)

            # Window Settings
            self.setFixedWidth(700)
            self.setFixedHeight(500)
            self.show()

        def DefineRoot(self):
            p = QFileDialog.getExistingDirectory(self, 'Open Root Directory to be FileMapped')
            self.rootLineEdit.setText(p)
            appInput["root_dir"] = p

        def JsonPath(self):
            j = QFileDialog.getSaveFileName(self, 'Save .json FileMap File', '', 'JSON Files (*.json)')
            self.jsonPathLineEdit.setText(j[0])
            appInput["json_path"] = j[0]

        def ExtOmits(self):
            o = self.extLineEdit.text()
            o = o.replace(' ', '')
            if o != '':
                appInput["ext_omits"] = o.split(',')
                omit_text = ''
                for omit in appInput["ext_omits"]:
                    if not omit.startswith('.'):
                        omit = '.' + omit
                    omit_text += omit
                    omit_text += ', '
                omit_text = omit_text[:-2]
                omit_text = 'Excluding the following extensions: ' + omit_text
                self.extOmitLabel.setText(omit_text)
            else:
                appInput["ext_omits"] = []
                omit_text = 'Excluding the following extensions: '
                self.extOmitLabel.setText(omit_text)

        def Generate(self):
            if (appInput["root_dir"] != "UNDEFINED") and (appInput["json_path"] != "UNDEFINED"):
                self.statusLabel.setText("Status: RUNNING")
                file_map = FileMapper(root_dir=appInput["root_dir"],
                                      extensions2omit=appInput["ext_omits"])
                json_object = json.dumps(file_map, indent=4)
                f = open(appInput["json_path"], "w")
                f.write(json_object)
                f.close()
                appInput["generated"] = True
                self.statusLabel.setText("Status: DONE!")
                self.outputButton.setText("Open " + os.path.basename(appInput["json_path"]))
            elif appInput["root_dir"] == "UNDEFINED":
                self.statusLabel.setText("Status: Root Dir Undefined!")
            else:
                self.statusLabel.setText("Status: JSON Path Undefined!")

        def GoToOutPutDir(self):
            if appInput["generated"]:
                os.startfile(os.path.dirname(appInput["json_path"]))

        def GoToFile(self):
            if appInput["generated"]:
                os.startfile(appInput["json_path"])

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
