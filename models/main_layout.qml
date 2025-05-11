import QtQuick
import Qt.labs.qmlmodels
import QtQuick.Layouts 
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Controls.Material

import io.qt.textproperties 1.0

ApplicationWindow {
    id: main_page
    title: 'Network Flow Viewer'
    width:1920
    height: 1080
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.Red

    GridLayout {
        id: grid
        columns: 2
        rows: 2
        anchors.fill: parent

        Pane {
            id: side_panel
            Layout.row: 0
            Layout.column: 0
            Layout.rowSpan: 2
            Layout.columnSpan: 1
            Layout.fillHeight: true
            Layout.preferredWidth: 200

            Material.elevation: 6
            Material.background: Material.Shade300

            ListView {
                width: 100
                height: 500
                model: columnOptionsModel

                delegate: CheckBox {
                    text: model.name
                    property bool isChecked: model.checked
                    checked: isChecked
                    onClicked: {
                        isChecked = !isChecked
                        columnOptionsModel.updateCheckedState(model.name, isChecked)
                    }
                }
            }
        }

        Pane {
            id: control_panel
            Layout.row: 0
            Layout.column: 1
            Layout.rowSpan: 1
            Layout.columnSpan: 1
            Layout.fillWidth: true
            Layout.preferredHeight: 150
            Layout.alignment: Qt.AlignTop

            Material.elevation: 6
            Material.background: Material.Shade400

            Row {
                spacing: 50

                DelayButton {
                    text: 'Install PMACCT'
                    delay: 500
                    onActivated: {
                        bridge.InstallPMACCT()
                    }
                }

                Button {
                    text: 'Start Capture'
                    onClicked: {
                        bridge.CaptureNetworkData()
                    }
                }
                signal toggleFriendlyNames(bool checked)

                CheckBox {
                    text: 'Use Friendly Names'
                    onCheckedChanged: {
                        bridge.toggleFriendlyNames(checked)
                    }
                }
            }
        }

        Pane {
            id: data_panel
            Layout.row: 1
            Layout.column: 1
            Layout.rowSpan: 1
            Layout.columnSpan: 1
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop

            Material.elevation: 6
            Material.background: Material.Brown

            TableView {
                model: networkDataModel
                anchors.fill: parent
                delegate: Rectangle {
                    implicitHeight: 50
                    implicitWidth: 100
                    border.width: 1

                    Text {
                        text: model.display
                    }
                }
            }
        }
    }
}