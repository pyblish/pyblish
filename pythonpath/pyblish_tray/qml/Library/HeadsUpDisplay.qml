import QtQuick 2.3


Item {
    id: root

    property bool active
    property Component background

    function notify(text) {
        animation.stop()
        active = true
        notificationText.text = text
        animation.restart()
    }

    Loader {
        id: widget
        anchors.horizontalCenter: parent.horizontalCenter
        width: notificationText.contentWidth + 20
        height: 30
        opacity: 0

        /*!
            Optional background shape
        */
        sourceComponent: background

        Text {
            id: notificationText
            z: 1
            color: "white"
            anchors.centerIn: widget
        }
    }

    SequentialAnimation {
        id: animation

        ParallelAnimation {
            NumberAnimation {
                target: widget
                properties: "y"
                duration: 200
                easing.type: Easing.OutCubic
                from: root.height / 2 - widget.height / 2 + 10
                to: root.height / 2 - widget.height / 2
            }

            NumberAnimation {
                target: widget
                duration: 100
                properties: "opacity"
                from: 0
                to: 1
            }
        }

        PauseAnimation {
            duration: 1000
        }

        NumberAnimation {
            target: widget
            properties: "opacity"
            from: 1
            to: 0
        }

        onStopped: {
            print("STOPPPED")
            root.active = false
        }
    }
}