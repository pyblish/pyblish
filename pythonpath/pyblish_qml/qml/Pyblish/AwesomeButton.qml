import QtQuick 2.3
import Pyblish 0.1

Ink {
    id: button

    property Action action

    property int elevation
    property color color: "white"

    property string name: action ? action.iconName : ""
    property int size: 14
    property double iconSize: 0

    property string style: "button"

    property int padding: 20

    width: view.width
    height: view.height

    onClicked: {
        if (action) action.triggered(icon)
    }

    View {
        id: view

        elevation: button.elevation

        width: button.size + 4
        height: button.size + 4

        AwesomeIcon {
            id: icon
            name: button.name
            color: button.color

            anchors.centerIn: parent

            size: button.iconSize || button.size
        }
    }
}
