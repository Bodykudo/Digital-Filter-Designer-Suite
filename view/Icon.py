from PyQt6 import QtGui


class Icon(QtGui.QIcon):
    def __init__(self, icon_path: str):
        super().__init__()
        self.addPixmap(
            QtGui.QPixmap(icon_path), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off
        )
