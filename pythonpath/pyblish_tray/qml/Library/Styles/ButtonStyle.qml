import QtQuick 2.3
import QtQuick.Controls.Styles 1.2

import Library 0.1


ButtonStyle {
    padding {
        left: 0
        right: 0
        top: 0
        bottom: 0
    }

    background: Rectangle {
        implicitWidth: 100
        implicitHeight: 35

        color: control.pressed ? Qt.darker(Theme.foreground, 0.5)
             : control.hovered ? Qt.darker(Theme.foreground, 0.1)
             : "transparent"
        border.width: 2
        border.color: Theme.highlight
    }

    label: Item {
        implicitWidth: label.width
        implicitHeight: label.height

        Text {
            id: label
            text: control.text

            anchors.centerIn: parent

            color: Theme.textColor
            font.family: Theme.boldFont
            font.pixelSize: 12
        }
    }
}
