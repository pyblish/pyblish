import QtQuick 2.3
import Pyblish 0.1


Item {
    id: progressBar

    property real progress: 0
    property color color: Theme.primaryColor

    clip: true

    Rectangle {
        id: bar

        x: -width * (1 - progressBar.progress)
        height: parent.height
        width: parent.width

        color: progressBar.color

        Behavior on x {
            NumberAnimation {
                duration: 100
            }
        }
    }
}