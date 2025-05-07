import QtQuick 2.15
import QtQuick.Layouts 1.11
import QtQuick.Controls 6.9 // 6.9 for the delay button
import QtQuick.Window 2.1
import QtQuick.Controls.Material 2.1

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
        rows: 3

        ColumnLayout {
            id: side_panel
            spacing: 2
            Layout.columnSpan: 1
            Layout.preferredWidth: 150
            Layout.topMargin: 10
            Layout.row: 0
            Layout.column: 0
            Layout.alignment: Qt.AlignLeft | Qt.AlignVTop

            ListView {
                width: 100
                height: 500
                model: columnOptionsModel

                delegate: CheckBox {
                    text: model.displayName
                    checked: model.isChecked
                    onCheckedChanged: columnOptionsModel.get(index).isChecked = checked
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
            Layout.preferredWidth: 1520
            Layout.topMargin: 10
            Layout.row: 1
            Layout.column: 1
            Layout.alignment: Qt.AlignTop

            TableView {
                ScrollBar.horizontal: ScrollBar {}
                ScrollBar.vertical: ScrollBar {}
                model: ['a', 'b', 'c']

                delegate: Rectangle {
                    Text {
                        text: modelData
                    }
                }
            }
        }
    }
}