import QtQuick 2.3


Item {
    property Flickable flickable

    visible: flickable.visibleArea.heightRatio < 1.0

    MouseArea {
        id: handle

        View {
            elevation: 1
            anchors.fill: parent
        }

        anchors.left: parent.left
        anchors.right: parent.right

        width: 20
        height: Math.max(30, flickable.visibleArea.heightRatio * flickable.height)

        y: !drag.active && !isNaN(flickable.visibleArea.heightRatio) ? (drag.maximumY * flickable.contentY) / (flickable.contentHeight * (1 - flickable.visibleArea.heightRatio)) : 0

        drag.target: handle
        drag.axis: Drag.YAxis
        drag.minimumY: 0
        drag.maximumY: flickable.height - handle.height
    }

    /*!
        Integration point
    */
    Binding {
        target: flickable
        property: "contentY"
        value: ((flickable.contentHeight * (1 - flickable.visibleArea.heightRatio)) * handle.y) / handle.drag.maximumY
        when: !flickable.moving && handle.drag.active && flickable !== undefined
    }
}