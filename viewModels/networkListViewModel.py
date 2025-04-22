from PySide6.QtCore import QAbstractListModel, QByteArray, QModelIndex, Qt, Slot
from PySide6.QtGui import QColor
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "NetworkListViewModel"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class NetworkListViewModel(QAbstractListModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.db)
    
    def setData(self, networks):
        print('setting network interface list')
        self.db = networks