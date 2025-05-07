from __future__ import annotations

import sys

from PySide6.QtCore import QObject, Signal, Slot, Property, QModelIndex, Qt, QAbstractListModel
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle

import pmacct.pmacct_helpers as pmacct

QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1

class ColumnOption(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = pmacct.GetColOptions()
        print('setting data as')
        for d in self._data:
            print(f'{d.displayName}, {d.isDefault}')

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._data):
            print('first')
            return None
        if role == Qt.DisplayRole:
            print('second')
            return self._data[index.row()]
        print('third')
        return None

@QmlElement
class Bridge(QObject):
    def __init__(self, columnModel):
        super().__init__()
        self.columnModel = columnModel

    @Slot()
    def InstallPMACCT(self):
        pmacct.InstallPMACCT()

    @Slot()
    def CaptureNetworkData(self):
        print('capturing data')

    @Slot(bool)
    def toggleFriendlyNames(self, useFriendlyNames):
        print(f'toggling names: {useFriendlyNames}')


if __name__ == '__main__':
    app = QGuiApplication(sys.argv)

    QQuickStyle.setStyle("Material")
    engine = QQmlApplicationEngine()

    columnOptionsModel = ColumnOption()
    bridge = Bridge(columnOptionsModel)

    context = engine.rootContext()
    context.setContextProperty("columnOptions", columnOptionsModel)
    context.setContextProperty("bridge", bridge)
    
    engine.addImportPath(sys.path[0])
    engine.loadFromModule("models", "main_layout")

    if not engine.rootObjects():
        sys.exit(-1)

    exit_code = app.exec()
    del engine
    sys.exit(exit_code)