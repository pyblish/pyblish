import QtQuick 2.3
import Pyblish 0.1


Rectangle {
    id: view

    width: 100
    height: 62

    color: "transparent"

    property int elevation

    property color __color: Theme.backgroundColor

    property int margins: 5

    Item {
        id: fill

        anchors.fill: parent

        visible: view.elevation != 0

        Rectangle {
            id: outerBorder

            color: Qt.darker(view.__color, view.elevation > 0 ? 0.9 : 1.2)
            radius: view.radius

            anchors {
                fill: parent
                margins: view.elevation > 0 ? 0 : 1
            }

            border {
                width: 1
                color: Qt.darker(view.__color, 2)
            }
        }

        Rectangle {
            id: innerBorder

            color: "transparent"
            radius: view.radius

            anchors {
                fill: parent
                margins: view.elevation > 0 ? 1 : 0
            }

            border {
                width: 1
                color: Qt.lighter(view.__color, 1.2)
            }
        }
    }
}