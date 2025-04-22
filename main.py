from __future__ import annotations

import sys

from PySide6.QtCore import QObject, Slot, QAbstractListModel, Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle

import pmacct.pmacct_helpers as pmacct
from viewModels.networkListViewModel import NetworkListViewModel

QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class Bridge(QObject):

    def __init__(self):
        super().__init__()
        self.networkInterfaceFilter = ''
        NetworkListViewModel.setData(self,['1','2','3'])

    @Slot(str, result=str)
    def updateFilter(self, s):
        self.networkInterfaceFilter = s

        
if __name__ == '__main__':

    app = QGuiApplication(sys.argv)

    QQuickStyle.setStyle("Material")
    engine = QQmlApplicationEngine()

    engine.addImportPath(sys.path[0])
    engine.loadFromModule("models", "main_layout")

    if not engine.rootObjects():
        sys.exit(-1)

    exit_code = app.exec()
    del engine
    sys.exit(exit_code)