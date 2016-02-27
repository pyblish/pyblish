import QtQuick 2.3

/*!
    \qmltype Selection

    \inqmlmodule Library 0.1

    \brief A visual indicator for selecting items in a ListView

    Example:

    \qml
    import QtQuick 2.3
    import Library 0.1

    Item {
        ListView {
            id: listView
            anchors.fill: parent
            interactive: false

            model: 10
            delegate: Text {
                text: modelData
            }
        }

        Selection {
            anchors.fill: parent
            listview: listView
            shape: Rectangle {
                color: "brown"
                opacity: 0.5
            }

            onSelectionChanged: print("Selecting from", startIndex, "to", endIndex)
        }
    }
*/
MouseArea {
    id: root

    /*!
        The component to draw upon click-dragging.
    */
    property Component shape

    /*!
        The parent ListView
    */
    property ListView listview

    signal selectionStarted(int startIndex, int endIndex)
    signal selectionChanged(int startIndex, int endIndex)
    signal selectionEnded(int startIndex, int endIndex)

    /*!
        Private variables
    */
    property rect __selection
    property int __startIndex
    property int __endIndex

    Loader {
        id: dragRect

        x: __selection.x
        y: __selection.y
        width: Math.max(1, __selection.width)
        height: Math.max(1, __selection.height)

        sourceComponent: shape

        active: false

        /*!
            Fade shape on release.
        */
        NumberAnimation {
            id: animation

            target: dragRect
            properties: "opacity"
            duration: 200
            from: 1
            to: 0

            onStopped: {
                dragRect.active = false
                dragRect.opacity = 1
                __selection = Qt.rect(0, 0, 0, 0)
            }
        }
    }

    onPressed: {
        animation.stop()

        __startIndex = listview.indexAt(0, listview.mapToItem(listview.contentItem, 0, mouse.y).y)
        __selection = Qt.rect(mouse.x, mouse.y, 0, 0)

        dragRect.active = true

        selectionStarted(__startIndex, __startIndex)
    }

    onPositionChanged: {
        __selection.width = mouse.x - __selection.x
        __selection.height = mouse.y - __selection.y

        __endIndex = listview.indexAt(0, listview.mapToItem(listview.contentItem, 0, mouse.y).y)
        __endIndex = __endIndex == -1 && mouse.y > 0 ? listview.count - 1 : __endIndex
        selectionChanged(__startIndex, __endIndex)
    }

    onReleased: {
        animation.restart()

        __endIndex = listview.indexAt(0, listview.mapToItem(listview.contentItem, 0, mouse.y).y)
        __endIndex = __endIndex == -1 && mouse.y > 0 ? listview.count - 1 : __endIndex
        selectionEnded(__startIndex, __endIndex)
    }
}