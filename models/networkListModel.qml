import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    property int modelIndex

    anchors {
        horizontalCenter: parent.horizontalCenter
        verticalCenter: parent.verticalCenter
    }

    TextArea {
        id: zone
        anchors.centerIn: parent
        text: display
    }

    MouseArea {
        id: zoneMouseArea
        anchors.fill: parent

        onClicked: lv.model.test(index)
    }
}