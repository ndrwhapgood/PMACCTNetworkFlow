#TODO: Modify pmacct helpers to use script instead of hard coded commands
# Add rest of pmacct columns and friendly names.
# Fix a bug where when the Friendy Name is selected, the selected column doesn't filter properly
#   To reproduct: select a column with a friendly name and friendly names enabled
#   Request data,
#   Deselect with the friendly name and request data again

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
        self._useFriendlyNames = False

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._data):
            return None
        elif role == Qt.DisplayRole:
            return self._data[index.row()]['friendlyName'] if self._useFriendlyNames else self._data[index.row()]['name']
        elif role == Qt.CheckStateRole:
            return Qt.Checked if self._data[index.row()]['checked'] else Qt.Unchecked
        elif role == Qt.UserRole: # Define a custom role for 'checked'
            return self._data[index.row()]['checked']
        return True
    
    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.UserRole:
            self._data[index.row()]['checked'] = value
            self.dataChanged.emit(index, index, [Qt.UserRole])
            return True
        return False
    
    def roleNames(self):
        return {Qt.DisplayRole: b'name', Qt.UserRole: b'checked'}

    def toggleFriendlyName(self):
        self._useFriendlyNames = not self._useFriendlyNames
        self.notifyChange()

    def notifyChange(self):
        for data in self._data:
            i = self._data.index(data)
            self.dataChanged.emit(self.index(i, 0), self.index(i, 0), Qt.UserRole)

    @Slot(str, bool)
    def updateCheckedState(self, name, checked):
        for data in self._data:
            if data['name'] == name:
                i = self._data.index(data)
                qml_index = self.index(i, 0)
                self.setData(qml_index, checked, Qt.UserRole)

    def getSelectedColsDisplayName(self):
        return list(map(lambda c: c['friendlyName'] if c['checked'] and self._useFriendlyNames else c['name'], self._data))

class DataTableModel(QAbstractTableModel):
    def __init__(self, data=[], headers=[]):
        super().__init__()
        self._data = data
        self._headers = headers
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._data)
    
    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0]) if self._data else 0
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount() and 0 <= index.column() < self.columnCount()):
            return None
        if role == Qt.DisplayRole or role == Qt.UserRole:
            return str(self._data[index.row()][index.column()])
        return None
        
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return None
    
    def setData(self, index, value, role=Qt.EditRole):
        if role==Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, {Qt.DisplayRole, Qt.EditRole})
            return True
        return False
    
    def updateData(self, headers, data):
        self._data = data
        self.updateHeaders(headers)
        self.notifyChange()

    def updateHeaders(self, headers):
        self.beginResetModel()
        self._headers = headers
        self.endResetModel()
        return True
    
    def notifyChange(self):
        for data in self._data:
            i = self._data.index(data)
            self.dataChanged.emit(self.index(i, 0), self.index(i, 0), Qt.DisplayRole)

    def swapHeaderColumn(self, cols=[]):
        # if len(self._data) > 0 and len(self._data[0]) == len(cols):
        #TODO: clean up and test more
        self.beginResetModel()
        self._headers = cols
        self.endResetModel()
        self._data[0] = cols
        self.notifyChange()

@QmlElement
class Bridge(QObject):
    def __init__(self, columnModel, dataModel):
        super().__init__()
        self.columnOptionsModel = columnModel
        self.dataModel = dataModel

    @Slot()
    def InstallPMACCT(self):
        result = pmacct.InstallPMACCT()
        print(result.stdout) # result.stderr expected to be ''

    @Slot()
    def CaptureNetworkData(self):
        cols = self.getSelectedColumns()
        data = pmacct.ParseData(cols)
        self.dataModel.updateData(cols, data)

    @Slot(bool)
    def toggleFriendlyNames(self, state):
        self.columnOptionsModel.toggleFriendlyName()
        new_headers = self.columnOptionsModel.getSelectedColsDisplayName()
        self.dataModel.swapHeaderColumn(new_headers)
        return self.columnOptionsModel._useFriendlyNames

    def getSelectedColumns(self):
        selectedCols = []
        #not a good way to do this, improve later.
        for co in self.columnOptionsModel._data:
            if co['checked']:
                selectedCols.append(co['name'])
        return selectedCols
    
if __name__ == '__main__':
    app = QGuiApplication(sys.argv)

    QQuickStyle.setStyle("Material")
    engine = QQmlApplicationEngine()

    columnOptionsModel = ColumnOption()
    networkDataModel = DataTableModel()

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