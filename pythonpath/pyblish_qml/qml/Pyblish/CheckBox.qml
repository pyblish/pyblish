import QtQuick 2.3
import Pyblish 0.1


MouseArea {
    id: checkView

    width: 10
    height: 10

    property bool active: true
    property bool checked: false

    property var statuses: {
        "default": "white",
        "processing": Theme.primaryColor,
        "success": Theme.dark.successColor,
        "warning": Theme.dark.warningColor,
        "error": Theme.dark.errorColor
    }

    property string status: "default"

    onStatusChanged: glow.opacity = 1

    AwesomeIcon {
        id: check

        name: "check"
        size: 8

        anchors.centerIn: parent

        color: statuses[status]
        opacity: checkView.checked ? checkView.active ? 1 : 0.5 : 0

        Behavior on opacity {
            NumberAnimation {
                duration: 100
            }
        }

        Behavior on color {
            ColorAnimation {
                from: "white"
                duration: 100
            }
        }
    }

    Rectangle {
        id: glow

        opacity: checkView.active ? 1 : 0.5

        width: Math.min(parent.width, parent.height)
        height: width

        anchors.centerIn: parent

        color: "transparent"
        border.color: check.color
        border.width: 1
    }
}
