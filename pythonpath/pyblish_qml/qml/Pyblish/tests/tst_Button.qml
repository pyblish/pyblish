import QtQuick 2.3
import Pyblish 0.1


Rectangle {
    id: root

    height: 300
    width: 300

    color: "brown"

    Column {
        spacing: 10
        
        anchors.fill: parent
        anchors.margins: 10
        
        Button {
            width: parent.width
            text: "Button Standard"
        }

        Button {
            text: "Button Elevated"
            width: parent.width
            elevation: 1
        }

        Button {
            text: "Button Elevated Inward"
            width: parent.width
            elevation: -1
        }
    }
}