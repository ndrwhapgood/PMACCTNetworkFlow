import QtQuick 2.0
import QtQuick.Layouts 1.11
import QtQuick.Controls 2.1
import QtQuick.Window 2.1
import QtQuick.Controls.Material 2.1
import NetworkListViewModel

import io.qt.textproperties 1.0

ApplicationWindow {
    id: main_page
    width:1920
    height: 1080
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.Red

    Bridge {
        id: bridge
    }

    GridLayout{
        id: grid
        columns: 2
        rows: 3

        ColumnLayout {
            id: side_panel
            spacing: 2
            Layout.columnSpan: 1
            Layout.preferredWidth: 400
            Layout.topMargin: 10
            
            TextField {
                id: filter
                Layout.alignment: Qt.AlignHCenter
                placeholderText: qsTr("enter name")
                onTextChanged: bridge.updateFilter(text)
                Layout.preferredWidth: 200
            }

            ListView {
                id: lv
                model: NetworkListViewModel {}
            }
        }
    }
}

// | <filter box> col 1, row 1    | <user_controls> col 2, row 1
// | <list of available networks> |____________________________
// | col 1, row 2                 |<network information table>
// |                              | col 2, row 2
//_____________________________________________
// | <status window>
// | col span 2, row 3