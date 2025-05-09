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

    GridLayout{
        id: grid
        columns: 2
        rows: 2

        ColumnLayout {
            id: side_panel
            spacing: 2
            Layout.columnSpan: 1
            Layout.preferredWidth: 300
            Layout.topMargin: 10
            Layout.row: 0
            Layout.column: 0
            Layout.alignment: Qt.AlignLeft | Qt.AlignVTop

            ListView {
                width: 100
                height: 500
                model: columnOptionsModel

                delegate: CheckBox {
                    text: model.display
                    //checked: model.checked
                }
            }
        }

        ColumnLayout {
            id: user_controls
            spacing: 2
            Layout.columnSpan: 1
            Layout.preferredWidth: 1470
            Layout.topMargin: 10
            Layout.row: 0
            Layout.column: 1
            Layout.alignment: Qt.AlignTop

            Rectangle {
                RowLayout {
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
        }

        ColumnLayout {
            id: data_view
            spacing: 2
            Layout.columnSpan: 1
            Layout.preferredWidth: 1470
            Layout.topMargin: 10
            Layout.row: 1
            Layout.column: 1
            Layout.alignment: Qt.AlignLeft | Qt.AlignVTop

            TableView {
                width: 1470
                height: 1000

                model: bridge.getTableModel()

                delegate: Text {
                    text: display
                }

                // model: TableModel {
                //     TableModelColumn { display: "name" }
                //     TableModelColumn { display: "color" }

                //     rows: [
                //         {
                //             "name": "cat",
                //             "color": "black"
                //         },
                //         {
                //             "name": "dog",
                //             "color": "brown"
                //         },
                //         {
                //             "name": "bird",
                //             "color": "white"
                //         }
                //     ]
                // }

                // delegate: Text {
                //     text: display
                // }
            }
        }
    }
}