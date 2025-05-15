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
    width: Screen.width
    height: Screen.height
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.Purple

    GridLayout {
        id: grid
        columns: 5
        rows: 3
        anchors.fill: parent

        Pane {
            id: side_panel
            Layout.row: 0
            Layout.column: 0
            Layout.rowSpan: 3
            Layout.columnSpan: 1
            Layout.fillHeight: true
            Layout.preferredWidth: 200

            Material.elevation: 6

            ComboBox {
                id: network_interfaces
                model: networkInterfaceModel
                anchors.top: parent.top
                textRole: 'display'

                onActivated: {
                    bridge.setNetworkInterface(network_interfaces.currentText)
                }
            }

            ListView {
                width: 100
                anchors.topMargin: network_interfaces.height
                anchors.fill: parent
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
            id: capture_panel
            Layout.row: 0
            Layout.column: 1
            Layout.rowSpan: 1
            Layout.columnSpan: 4
            Layout.fillWidth: true
            Layout.preferredHeight: 150
            Layout.alignment: Qt.AlignTop

            Material.elevation: 6

            RowLayout {
                anchors.fill: parent
                ColumnLayout {
                    RowLayout {
                        Button {
                            id: captureButton
                            text: 'Start Capture'
                            enabled: bridge.enableStartButton
                            onClicked: {
                                bridge.captureNetworkData()
                                bridge.toggleStartButton()
                            }
                        }
                        signal toggleFriendlyNames(bool checked)
                    }

                    RowLayout {
                        CheckBox {
                            text: 'Use Friendly Names'
                            onCheckedChanged: {
                                bridge.toggleFriendlyNames(checked)
                            }
                        }
                    }
                }
                ColumnLayout {
                    RowLayout {
                        Button {
                            text: 'Update'
                            onClicked: {
                                bridge.updateData()
                            }
                        }
                    }
                    RowLayout {
                        Button {
                            text: 'Stop'
                            onClicked: {
                                bridge.killDeamon()
                                bridge.toggleStartButton()
                            }
                        }
                    }
                }

                ColumnLayout {
                    RowLayout {
                        TextField {
                            id: limit
                            width: 150
                            placeholderText: 'Row Limit'

                            onTextChanged: {
                                bridge.updateRowLimit(limit.text)
                            }

                            Component.onCompleted: {
                                if (text === '') {
                                    text = '100'
                                }
                            }
                        }
                        TextField {
                            id: filter
                            width: 150
                            placeholderText: 'Filter'

                            onTextChanged: {
                                bridge.updateFilter(filter.text)
                            }
                        }
                    }
                }

                ColumnLayout {
                    Layout.alignment: Qt.AlignRight
                    // empty row to push the button in the corner.
                    RowLayout { }

                    RowLayout {
                        DelayButton {
                            Layout.topMargin: 10
                            text: 'Install'
                            delay: 500
                            onActivated: {
                                bridge.InstallPMACCT()
                            }
                        }
                    }
                }
            }
        }

        Pane {
            id: data_panel
            Layout.row: 1
            Layout.column: 1
            Layout.rowSpan: 1
            Layout.columnSpan: 2
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop

            Material.elevation: 6

            TableView {
                model: networkDataModel
                anchors.fill: parent

                delegate: Item {
                    implicitHeight: 30
                    implicitWidth: 175

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

        Pane {
            id: fun_facts
            Layout.row: 2
            Layout.column: 1
            Layout.rowSpan: 1
            Layout.columnSpan: 1
            Layout.fillWidth: true
            height: 300

            Material.elevation: 6

            Text {
                text: 'fun facts'
                color: 'white'
            }
        }

        Pane {
            id: save_panel
            Layout.row: 2
            Layout.column: 2
            Layout.rowSpan: 1
            Layout.columnSpan: 1
            Layout.fillWidth: true
            height: 300

            Material.elevation: 6
            
            Button {
                text: 'Save'
                anchors.right: parent.right
                onClicked: {
                    bridge.saveData()
                }
            }
        }
    }
}