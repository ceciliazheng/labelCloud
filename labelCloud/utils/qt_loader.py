from pathlib import Path
from PySide6.QtCore import QFile, QDir
from PySide6.QtUiTools import QUiLoader


class UiLoader(QUiLoader):
    def __init__(self, baseinstance, customWidgets=None):
        super().__init__(baseinstance)
        self.baseinstance = baseinstance
        if customWidgets:
            for name, obj in customWidgets.items():
                self.registerCustomWidget(obj)

    def createWidget(self, class_name, parent=None, name=""):
        if parent is None and self.baseinstance:
            return self.baseinstance
        else:
            return super().createWidget(class_name, parent, name)


def loadUi(ui_path, baseinstance, customWidgets=None):
    loader = UiLoader(baseinstance, customWidgets)
    ui_file = QFile(ui_path)
    # Set the working directory to the ui file's directory so that relative paths in the UI file work
    loader.setWorkingDirectory(QDir(str(Path(ui_path).parent)))
    ui_file.open(QFile.ReadOnly)
    loader.load(ui_file)
    ui_file.close()
