from os import path

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QFormLayout,
    QFileDialog,
    QLineEdit,
    QMessageBox,
    QRadioButton,
    QButtonGroup,
)

from converter.converter_3ds import Converter3DS
from converter.converter_wiiu import ConverterWiiU


class App:
    def start(self):
        app = QApplication([])

        app.setStyle("Fusion")

        self.window = QWidget()
        self.window.setWindowTitle("MH3U Save Converter")
        self.window.setMinimumWidth(600)

        layout = QFormLayout()

        # Source file
        self.srcPath = QLineEdit()
        loadSrcButton = QPushButton("Select save")
        loadSrcButton.clicked.connect(self.loadSrc)

        layout.addRow(loadSrcButton, self.srcPath)

        # Conversion type
        self.toWiiU = QRadioButton("3DS → Wii U")
        self.to3DS = QRadioButton("Wii U → 3DS")

        self.toWiiU.setChecked(True)

        self.conversionGroup = QButtonGroup()
        self.conversionGroup.addButton(self.toWiiU)
        self.conversionGroup.addButton(self.to3DS)

        layout.addRow("Convert:", self.toWiiU)
        layout.addRow("", self.to3DS)

        # Destination file
        self.dstPath = QLineEdit()
        setOutputButton = QPushButton("Select output")
        setOutputButton.clicked.connect(self.setDst)

        layout.addRow(setOutputButton, self.dstPath)

        # Convert button
        convertButton = QPushButton("Convert")
        convertButton.clicked.connect(self.convert)

        layout.addRow(convertButton)

        self.window.setLayout(layout)
        self.window.show()

        app.exec()

    def loadSrc(self):
        filePath = QFileDialog.getOpenFileName(
            self.window,
            "Select MH3U save file"
        )

        if filePath[0]:
            self.srcPath.setText(filePath[0])

    def setDst(self):
        filePath = QFileDialog.getSaveFileName(
            self.window,
            "Select output file"
        )

        if filePath[0]:
            self.dstPath.setText(filePath[0])

    def convert(self):
        srcPath = self.srcPath.text()
        dstPath = self.dstPath.text()

        if not path.exists(srcPath):
            QMessageBox.warning(
                self.window,
                "Invalid save",
                "The selected save file does not exist."
            )
            return

        if not dstPath:
            QMessageBox.warning(
                self.window,
                "Output missing",
                "Please select an output file."
            )
            return

        try:
            if self.toWiiU.isChecked():
                converter = ConverterWiiU(srcPath)
            else:
                converter = Converter3DS(srcPath)

            converter.convert(dstPath)

        except Exception as error:
            QMessageBox.critical(
                self.window,
                "Conversion error",
                f"The conversion failed:\n\n{error}"
            )
            return

        QMessageBox.information(
            self.window,
            "Success",
            "File converted successfully."
        )


if __name__ == "__main__":
    App().start()
