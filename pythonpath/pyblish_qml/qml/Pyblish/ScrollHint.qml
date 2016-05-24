import QtQuick 2.0


Item {
    property Flickable flickable

    visible: flickable.visibleArea.heightRatio < 1.0

    SequentialAnimation on opacity{
        loops: Animation.Infinite

        PauseAnimation { duration: 500 }

        NumberAnimation {
            duration: 500
            from: 1
            to: 0.5
            easing.type: Easing.InOutCubic
        }
        NumberAnimation {
            duration: 500
            from: 0.5
            to: 1
            easing.type: Easing.InOutCubic
        }
    }

    Label {
        text: "Scroll"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 20
    }

    AwesomeIcon {
        id: arrow

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0

        name: "caret-down"
        size: 20
        opacity: 0

        SequentialAnimation {
            running: true
            loops: Animation.Infinite

            ParallelAnimation {
                NumberAnimation {
                    target: arrow
                    property: "anchors.bottomMargin"
                    from: -30
                    to: 0
                    duration: 0
                }
                NumberAnimation {
                    target: arrow
                    property: "opacity"
                    from: 0
                    to: 1
                    duration: 200
                }
            }

            PauseAnimation { duration: 1000 }

            ParallelAnimation {
                NumberAnimation {
                    target: arrow
                    property: "anchors.bottomMargin"
                    from: 0
                    to: -30
                    easing.type: Easing.InQuint
                    duration: 1000
                }
                NumberAnimation {
                    target: arrow
                    property: "opacity"
                    from: 1
                    to: 0
                    easing.type: Easing.InQuint
                    duration: 1000
                }
            }
        }
    }
}
