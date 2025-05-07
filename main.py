#TODO: QML - make list delegate show checkbox and correct text
#            data table model and delegate
#      Python - parse csv data

from __future__ import annotations

import sys

from PySide6.QtCore import QObject, Slot, QModelIndex, Qt, QAbstractListModel, QAbstractTableModel
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

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)
    
    def data(self, index):
        if not index.isValid() or index.row() >= len(self._data):
            return None
        return self._data[index.row()]
    
    def ToggleDisplayName(self, useFriendly):
        for col in self._data:
            col.displayName = col.friendlyName if useFriendly else col.name

    def GetCheckedCols(self):
        return list(filter(lambda x: x.isChecked, self._data)) 

class DataTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

@QmlElement
class Bridge(QObject):
    def __init__(self, columnModel, dataModel):
        super().__init__()
        self.columnOptionsModel = columnModel
        self.dataModel = dataModel

    @Slot()
    def InstallPMACCT(self):
        pmacct.InstallPMACCT()

    @Slot()
    def CaptureNetworkData(self):
        print('capturing data')

    @Slot(bool)
    def toggleFriendlyNames(self, useFriendlyNames):
        print(f'toggling names: {useFriendlyNames}')
        self.columnOptionsModel.ToggleDisplayName(useFriendlyNames)

    def GetTableHeaders(self):
        headers = self.columnOptionsModel.GetCheckedCols()

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)

    QQuickStyle.setStyle("Material")
    engine = QQmlApplicationEngine()

    columnOptionsModel = ColumnOption()
    dataTableModel = DataTableModel()

    bridge = Bridge(columnOptionsModel, dataTableModel)

    context = engine.rootContext()
    context.setContextProperty("columnOptionsModel", columnOptionsModel)
    context.setContextProperty("dataTable", dataTableModel)
    context.setContextProperty("bridge", bridge)
    
    engine.addImportPath(sys.path[0])
    engine.loadFromModule("models", "main_layout")

    if not engine.rootObjects():
        sys.exit(-1)

    exit_code = app.exec()
    del engine
    sys.exit(exit_code)