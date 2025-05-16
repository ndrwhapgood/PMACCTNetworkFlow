#TODO: refresh data async
# fix button enable/disable logic
# Do a global check if pmacct is install, disable Start button if not.
# More bug fixes when I just start clicking things too much.
# Put network interface model in it's own row so the other stuff doesn't show up behind it.

from __future__ import annotations

import sys
import time

from PySide6.QtCore import QObject, Slot, QModelIndex, Qt, QAbstractListModel, QAbstractTableModel, Property, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle

import pmacct.pmacct_helpers as pmacct

QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1


class NetworkInterfaceModel(QAbstractListModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = pmacct.GetNetworkInterfaces()

    def rowCount(self, parent=None):
        return len(self._data)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._data):
            return None
        if role == Qt.DisplayRole:
            return self._data[index.row()]
        return True
    
    def setData(self, index, value, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            self._data[index.row()] = value
            self.dataChanged.emit(index, index, [Qt.EditRole | Qt.DisplayRole])
            return True
        return False

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

    def isChecked(self, c):
        return c['checked']

    def getSelectedColsDisplayName(self):
        checked_cols = filter(self.isChecked, self._data)
        return list(map(lambda c: c['friendlyName'] if self._useFriendlyNames else c['name'], checked_cols))
    
    def getSelectedColIndexes(self):
        return list(map(lambda x: self._data.index(x), filter(lambda x: x['checked'], self._data)))
    
    def getDisplayNames(self):
        return list(map(lambda c: c['friendlyName'] if self._useFriendlyNames else c['name'], self._data))

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
    
    def updateData(self, indexes, headers, table):
        # filter data based on indexes
        headers = [headers[i] for i in indexes]
        data = []
        for row in table:
            # data needs to be appened like this to save the data and not the object.
            d = [row[i] for i in indexes]
            data.append(d)
        self._data = data
        self._data.insert(0, headers)
        self.notifyChange()
        self.updateHeaders(headers)

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
        if len(self._data) > 0 and len(self._data[0]) == len(cols):
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
        self.selectedInterface = pmacct.GetNetworkInterfaces()[0] #hopefully this is never empty
        self._enableStartButton = True
        self.rowLimit = 100
        self.dataFilter = ''
        self._funFacts = ':)'

    buttonEnabledChanged = Signal()

    @Property(bool, notify=buttonEnabledChanged)
    def enableStartButton(self):
        return self._enableStartButton
    
    @enableStartButton.setter
    def enableStartButton(self, value):
        if self._enableStartButton != value:
            self._enableStartButton = value
            self.buttonEnabledChanged.emit()

    @Slot()
    def toggleStartButton(self):
        self._enableStartButton = not self._enableStartButton
        self.enableStartbuttonChanged.emit(self._enableStartButton)

    @Slot()
    def InstallPMACCT(self):
        pmacct.InstallPMACCT()

    @Slot()
    def captureNetworkData(self):
        indexes = self.columnOptionsModel.getSelectedColIndexes()
        pmacct.StartDaemon(self.selectedInterface)
        time.sleep(1) # bad way of doing this, improve later
        data = pmacct.GetData(self.rowLimit)
        headers = self.columnOptionsModel.getDisplayNames()
        self.dataModel.updateData(indexes, headers, data)

    @Slot(bool)
    def toggleFriendlyNames(self, state):
        self.columnOptionsModel.toggleFriendlyName()
        new_headers = self.columnOptionsModel.getSelectedColsDisplayName()
        self.dataModel.swapHeaderColumn(new_headers)
        return self.columnOptionsModel._useFriendlyNames
    
    @Slot(str)
    def setNetworkInterface(self, interface):
        self.selectedInterface = interface

    @Slot(str)
    def updateRowLimit(self, limit):
        try:
            self.rowLimit = int(limit)
        except ValueError:
            self.rowLimit = 100

    @Slot(str)
    def updateFilter(self, f):
        self.dataFilter = f

    def buildFilter(self):
        #make this check more robust.
        if len(self.dataFilter) < 5:
            return {}
        # simple filter
        # expected input <name>, value; <name>, value
        # output {<name>: <value>}
        f = {}
        for i in self.dataFilter.split(';'):
            f[i.split(',')[0]] = i.split(',')[1]

        return f

    @Slot()
    def killDeamon(self):
        pmacct.KillDaemon()

    @Slot()
    def updateData(self):
        indexes = self.columnOptionsModel.getSelectedColIndexes()
        data = pmacct.GetDataV2(self.rowLimit, self.buildFilter())
        headers = self.columnOptionsModel.getDisplayNames()
        self.dataModel.updateData(indexes, headers, data)
        self._funFacts = " ".join(pmacct.GetFunFacts())
        self.funFactsChanged.emit(" ".join(pmacct.GetFunFacts()))
        
        print(self._funFacts)

    @Slot()
    def saveData(self):
        pmacct.SaveData(self.columnOptionsModel.getSelectedColIndexes())

    enableStartbuttonChanged = Signal(bool)

    @Property(bool, notify=enableStartbuttonChanged)
    def enableStartButton(self):
        return self._enableStartButton
    
    @enableStartButton.setter
    def enableStartButton(self, value):
        self._enableStartButton = value
        self.enableStartbuttonChanged.emit()

    funFactsChanged = Signal(str)

    @Property(str, notify=funFactsChanged)
    def funFacts(self):
        return self._funFacts
    
    @funFacts.setter
    def funFacts(self, value):
        self._funFacts = value
        self.funFactsChanged.emit()
    
if __name__ == '__main__':
    pmacct.Init()
    app = QGuiApplication(sys.argv)

    QQuickStyle.setStyle("Material")
    engine = QQmlApplicationEngine()

    networkInterfaceModel = NetworkInterfaceModel()
    columnOptionsModel = ColumnOption()
    networkDataModel = DataTableModel()

    bridge = Bridge(columnOptionsModel, networkDataModel)

    context = engine.rootContext()
    context.setContextProperty("networkInterfaceModel",networkInterfaceModel)
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