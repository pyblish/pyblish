import QtQuick 2.3
import Pyblish 0.1

Ink {
    id: button

    property int elevation

    property string text
    property string icon

    property string style: "button"

    property int padding: 20
    
    width: Math.max(row.width,
                    label.width + padding,
                    10 + padding)
    height: 30

    View {
        id: view

        elevation: button.elevation

        anchors.fill: parent

        Row {
            id: row

            anchors.centerIn: parent
            spacing: 10

            Icon {
                anchors.verticalCenter: parent.verticalCenter
                name: button.icon
                visible: typeof button.icon != "undefined"
            }

            Label {
                id: label
                text: button.text
                style: button.style
                anchors.verticalCenter: parent.verticalCenter
            }
        }
    }
}