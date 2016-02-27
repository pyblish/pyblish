import QtQuick 2.3
import Pyblish 0.1


Label {
    id: message
    opacity: 0

    property alias animation: messageAnimation

    SequentialAnimation {
        id: messageAnimation

        ParallelAnimation {
            NumberAnimation {
                target: message
                property: "x"
                from: 5
                to: 20
                duration: 1000
                easing.type: Easing.OutQuint
            }
            NumberAnimation {
                target: message
                property: "opacity"
                from: 0
                to: 1
                duration: 500
                easing.type: Easing.OutQuint
            }
        }

        PauseAnimation {
            duration: 1000
        }

        NumberAnimation {
            target: message
            property: "opacity"
            to: 0
            duration: 2000
        }
    }
}