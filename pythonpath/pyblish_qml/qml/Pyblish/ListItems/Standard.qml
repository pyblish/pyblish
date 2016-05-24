import QtQuick 2.3
import Pyblish 0.1
import Pyblish.ListItems 0.1


BaseListItem {
    id: listItem

    property bool active: false
    property bool checked: false
    property alias status: indicator.status

    property alias text: label.text

    property int margins: 5

    Row {
        spacing: 5
        anchors.fill: parent
        anchors.leftMargin: listItem.margins
        anchors.rightMargin: listItem.margins

        CheckBox {
            id: indicator
            active: listItem.active
            opacity: active ? 1.0 : 0.5
            checked: listItem.checked
            anchors.verticalCenter: parent.verticalCenter

            onClicked: {
                listItem.clicked(mouse)
            }
        }

        Label {
            id: label
            opacity: active ? 1.0 : 0.5
            anchors.verticalCenter: parent.verticalCenter

            Behavior on color {
                ColorAnimation {
                    duration: 100
                }
            }
        }
    }
}
