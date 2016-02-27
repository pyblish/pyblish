import QtQuick 2.3
import Pyblish 0.1


Rectangle {
    id: parentItem

    width: 500
    height: 300

    color: "brown"

    Rectangle {
        width: 50
        height: 50

        anchors.centerIn: parent

        radius: parent.width / 2

        MouseArea {
            anchors.fill: parent

            property Item tooltip

            hoverEnabled: true
            onEntered: {
                this.tooltip = Tooltip.create("This is an amazing tooltip", parent)
                this.tooltip.show()
            }
            onExited: this.tooltip.hide()
        }
    }
}
