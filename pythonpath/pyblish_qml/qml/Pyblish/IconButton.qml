import QtQuick 2.0
import Pyblish 0.1


Button {
    id: icon

    signal triggered

    property Action action

    style: "body1"

    text: action ? action.name : ""
    icon: action ? action.iconName : ""
    
    enabled: action ? action.enabled : true

    padding: 40

    onTriggered: {
        if (action) action.triggered(icon)
    }

    opacity: enabled ? 1 : 0.6

    onClicked: {
        icon.triggered()
    }
}