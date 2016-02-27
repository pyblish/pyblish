import QtQuick 2.0

Item {
   id: scrollbar

    property Flickable flickable : undefined

    anchors.right: flickable.right;
    anchors.top: flickable.top
    anchors.bottom: flickable.bottom

    visible: flickable.visible

    width: ma.containsMouse || ma.drag.active ? 20 : 18

    Behavior on width {
        NumberAnimation {
            duration: 50
            easing.type: Easing.OutQuad
        }
    }

    Rectangle {
        id: handle

        anchors.left: parent.left
        anchors.right: parent.right

        height: flickable.visibleArea.heightRatio * flickable.height
        visible: flickable.visibleArea.heightRatio < 1.0

        color: "gray"

        opacity: ma.pressed ? 1 : ma.containsMouse ? 0.85 : 0.5

        Behavior on opacity {
            NumberAnimation {
                duration: 150
            }
        }

        Binding {
            target: handle
            property: "y"
            value: !isNaN(flickable.visibleArea.heightRatio) ? (ma.drag.maximumY * flickable.contentY) / (flickable.contentHeight * (1 - flickable.visibleArea.heightRatio)) : 0
            when: !ma.drag.active
        }

        Binding {
            target: flickable
            property: "contentY"
            value: ((flickable.contentHeight * (1 - flickable.visibleArea.heightRatio)) * handle.y) / ma.drag.maximumY
            when: ma.drag.active && flickable !== undefined
        }

        MouseArea {
            id: ma
            anchors.fill: parent
            hoverEnabled: true
            drag.target: parent
            drag.axis: Drag.YAxis
            drag.minimumY: 0
            drag.maximumY: flickable.height - handle.height
            preventStealing: true
        }
    }
}