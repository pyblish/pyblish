import QtQuick 2.3
import Pyblish 0.1


BaseListItem {
    id: listItem

    property bool active: false
    property bool checked: false
    property alias status: indicator.status

    property alias text: label.text
    property alias subText: subLabel.text

    property int margins: 5

    height: 40

    Row {
        spacing: 10
        anchors.fill: parent
        anchors.leftMargin: listItem.margins
        anchors.rightMargin: listItem.margins

        CheckBox {
            id: indicator
            active: listItem.active
            checked: listItem.checked
            anchors.verticalCenter: parent.verticalCenter

            onClicked: {
                listItem.clicked(mouse)
            }
        }

        Column {
            width: parent.width
            anchors.verticalCenter: parent.verticalCenter

            Label {
                id: label
                opacity: active ? 1.0 : 0.5
                style: "body2"

                Behavior on color {
                    ColorAnimation {
                        duration: 100
                    }
                }
            }

            Label {
                id: subLabel

                color: Theme.dark.subTextColor
                elide: Text.ElideRight
                width: parent.width

                style: "body1"
                visible: text != ""
            }
        }
    }
}
