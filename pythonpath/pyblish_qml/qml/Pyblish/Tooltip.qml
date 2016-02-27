import QtQuick 2.2
import Pyblish 0.1
import "Tooltip.js" as Tooltip
 
Item {
    id: tooltip
 
    property alias text: tooltipText.text
    property string placement: "top"
 
    function show() {
        this.state = "shown"
    }
 
    function hide() {
        this.state = "hidden"
    }
 
    width: tooltipText.width + 20
    height: tooltipText.height + 10

    opacity: state == "shown" ? 1 : 0

    Behavior on opacity {
        NumberAnimation {
            duration: 50
        }
    }

    Rectangle {
        anchors.fill: parent

        color: "black"

        radius: 6

        Rectangle {
            id: arrow

            width: 7
            height: 7
            rotation: 45

            color: parent.color

            anchors.right: parent.right
            anchors.rightMargin: 8
            anchors.verticalCenter: parent.bottom
        }

        Label {
            id: tooltipText
            anchors.centerIn: parent
            horizontalAlignment: Text.AlignHCenter
        }
    }
  
    states: [
        State {
            name: "shown"
        },

        State {
            name: "hidden"
            onCompleted: tooltip.destroy()
        }
    ]
}