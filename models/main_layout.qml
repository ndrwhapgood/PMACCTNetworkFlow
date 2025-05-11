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

            Row {
                Button {
                    Layout.topMargin: 10
                    text: 'Start Capture'
                    onClicked: {
                        bridge.CaptureNetworkData()
                    }
                }
                signal toggleFriendlyNames(bool checked)

                CheckBox {
                    Layout.topMargin: 10
                    text: 'Use Friendly Names'
                    onCheckedChanged: {
                        bridge.toggleFriendlyNames(checked)
                    }
                }
            }

            DelayButton {
                Layout.topMargin: 10
                anchors.right: parent.right
                text: 'Install PMACCT'
                delay: 500
                onActivated: {
                    bridge.InstallPMACCT()
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

            TableView {
                model: networkDataModel
                anchors.fill: parent

                delegate: Item {
                    implicitHeight: 30
                    implicitWidth: 150

                    Item {
                        anchors.centerIn: parent

                        Text {
                            anchors.centerIn: parent
                            verticalAlignment: Text.AlignVCenter
                            text: model.display
                            color: 'white'
                        }
                    }
                }
            }
        }
    }
}