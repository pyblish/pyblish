import QtQuick 2.0

/*!
    \qmltype Scrollbar

    \inqmlmodule Library 0.1

    \brief Represents a scrollbar to be attached to a Flickable.

    Example:

    \qml
    import QtQuick 2.3
    import QtQuick.Controls 1.3
    import Library 0.1

    Item {
        Loader {
            id: loader
            source: {
                0: Qt.resolvedUrl("File1.qml"),
                1: Qt.resolvedUrl("File2.qml")
            }[tabBar.currentIndex]
        }

        TabBar {
            id: tabBar
            
            actions: [
                Action { iconName: "close" },
                Action { iconName: "hand-o-up" }
            ]

            anchors.fill: parent
        }
    }
*/
Item {

    /*!
        Parent Flickable component to associate scrollbar with
    */
    property Flickable flickable

    /*!
        Optional background Component
    */
    property alias background: backgroundLoader.sourceComponent

    /*!
        Optional foreground Component. Keep in mind that if
        there is no foreground, the current position of the
        scrollbar will not be visible.
    */
    property alias foreground: foregroundLoader.sourceComponent

    /*!
        Set to true to keep scrollbar visible even though
        there isn't enough content to justify scrolling.
    */
    property bool alwaysVisible: false

    /*!
        True when handle is being dragged.
    */
    readonly property bool active: handle.drag.active ? true : false
    readonly property double currentRatio: handle.y / handle.drag.maximumY
    readonly property alias currentY: handle.y

    visible: alwaysVisible || flickable.visibleArea.heightRatio < 1.0

    Loader {
        id: backgroundLoader
        anchors.fill: parent
    }

    MouseArea {
        id: handle

        width: parent.width
        height: Math.max(width, flickable.visibleArea.heightRatio * flickable.height)

        anchors {
            left: parent.left
            right: parent.right
        }

        Loader {
            id: foregroundLoader
            anchors.fill: parent
        }

        y: !drag.active && !isNaN(flickable.visibleArea.heightRatio) ? (drag.maximumY * flickable.contentY) / (flickable.contentHeight * (1 - flickable.visibleArea.heightRatio)) : 0

        drag.target: handle
        drag.axis: Drag.YAxis
        drag.minimumY: 0
        drag.maximumY: flickable.height
                       - handle.height
                       + flickable.anchors.topMargin
                       + flickable.anchors.bottomMargin
    }

    Binding {
        target: flickable
        property: "contentY"
        value: ((flickable.contentHeight * (1 - flickable.visibleArea.heightRatio)) * handle.y) / handle.drag.maximumY
        when: !flickable.moving && handle.drag.active && flickable !== undefined
    }
}