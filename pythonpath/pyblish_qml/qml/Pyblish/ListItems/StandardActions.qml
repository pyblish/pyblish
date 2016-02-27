import QtQuick 2.3
import Pyblish 0.1
import Pyblish.ListItems 0.1


MouseArea {
    id: listItem

    signal toggled(var mouse)
    signal rightClicked(var mouse)

    property bool active: false
    property bool checked: false
    property alias status: indicator.status

    property alias text: label.text

    property int margins: 5

    property list<Action> actions

    acceptedButtons: Qt.RightButton

    onClicked: rightClicked(mouse)

    Rectangle {
        anchors.fill: parent
        color: Theme.alpha("#000", 0.4)
        opacity: status == "processing" ? 1.0 : 0
        radius: 3

        Rectangle {
            anchors.fill: parent
            color: "transparent"
            border.color: "white"
            border.width: 1
            radius: 3
            visible: status == "processing" ? 1 : 0

            SequentialAnimation on opacity {
                running: true

                NumberAnimation {
                    from: .4
                    to: 1
                    duration: 800
                    easing.type: Easing.InOutElastic
                }
                NumberAnimation {
                    from: 1
                    to: .4
                    duration: 800
                    easing.type: Easing.InOutElastic
                }

                loops: Animation.Infinite
            }
        }
    }

    Row {
        id: body
        spacing: 5
        anchors.left: parent.left
        anchors.leftMargin: listItem.margins

        width: parent.width - parent.margins - head.width
        height: parent.height

        CheckBox {
            id: indicator

            active: listItem.active
            checked: listItem.checked

            height: parent.height

            anchors.verticalCenter: parent.verticalCenter

            onClicked: listItem.toggled(mouse)
        }

        Label {
            id: label
            opacity: active ? 1.0 : 0.5
            anchors.verticalCenter: parent.verticalCenter
            elide: Text.ElideRight

            Behavior on color {
                ColorAnimation {
                    duration: 100
                }
            }

            width: parent.width - parent.spacing - indicator.width - 10
        }
    }

    Row {
        id: head
        anchors.right: parent.right
        anchors.rightMargin: listItem.margins
        anchors.verticalCenter: parent.verticalCenter

        height: parent.height

        Repeater {
            model: listItem.actions

            AwesomeButton {
                action: modelData
                size: action.iconSize
                visible: action.enabled
                tooltip: action.tooltip
            }
        }
    }
}
