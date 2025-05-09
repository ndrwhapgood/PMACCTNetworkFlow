#TODO: Rendering the table to the model is causing it to crash
# Check boxes aren't binding correctly to the models isChecked property
# Modify pmacct helpers to use script instead of hard coded commands
# Write csv parser
# Add rest of pmacct columns and friendly names.

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
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._data):
            return None
        elif role == Qt.DisplayRole:
            return self._data[index.row()].displayName
        elif role == Qt.CheckStateRole:
            print(f'checked state role: {role}')
            return self._data[index.row()].isChecked
        return True
    
    def ToggleDisplayName(self, useFriendly):
        for col in self._data:
            col.displayName = col.friendlyName if useFriendly else col.name

    def GetCheckedCols(self):
        return list(filter(lambda x: x.isChecked, self._data)) 

class DataTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or []
        print('table init')
    
    def rowCount(self):
        return len(self._data)
    
    def columnCount(self):
        return len(self._data[0]) if self._data else 0
    
    def data(self, index, role=Qt.DisplayRole):
        print(f'table data {index} {role}')
        print(f'data {index} {role}')
        if not index.isValid() or not (0 <= index.row() < self.rowCount() and 0 <= index.column() < self.columnCount()):
            return None
        if role == Qt.DisplayRole or role == Qt.UserRole:
            return str(self._data[index.row()][index.column()])
        return None
        
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        print(f'table header {section} {role}')
        print(f'headerData {section} {orientation} {role}')
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return ['src_ip', 'dst_ip', 'proto'][section]
        return super().headerData(section, orientation, role)


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
        self.columnOptionsModel.ToggleDisplayName(useFriendlyNames)

    @Slot()
    def getTableModel(self):
        print('getting table model')
        print(f'{self.dataModel._data}')
        return self.dataModel

    # def GetTableHeaders(self):
    #     return self.columnOptionsModel.GetCheckedCols()

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)

    QQuickStyle.setStyle("Material")
    engine = QQmlApplicationEngine()

    test_data = [
        ['10.0.0.1', '192.0.0.1', 'tcp'],
        ['10.0.0.1', '192.0.0.2', 'tcp'],
        ['10.0.0.1', '192.0.0.3', 'udp']
    ]

    columnOptionsModel = ColumnOption()
    networkDataModel = DataTableModel(test_data)

    bridge = Bridge(columnOptionsModel, networkDataModel)

    context = engine.rootContext()
    context.setContextProperty("columnOptionsModel", columnOptionsModel)
    context.setContextProperty("networkDataModel", networkDataModel)
    context.setContextProperty("bridge", bridge)
    
    engine.addImportPath(sys.path[0])
    engine.loadFromModule("models", "main_layout")

    if not engine.rootObjects():
        sys.exit(-1)

    exit_code = app.exec()
    del engine
    sys.exit(exit_code)