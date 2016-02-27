/*
 * Example of composite items with bindings
 *
 * When the item is clicked, it's creator-specific height
 * is used to determine the height of the overall item.
 *
*/

import QtQuick 2.3

MouseArea {
    id: composite

    property bool expanded

    property Component body

    property alias bodyItem: bodyLoader.item

    clip: true

    Row {
        anchors.fill: parent

        Rectangle {
            color: "brown"
            width: 50
            height: parent.height
        }

        Loader {
            id: bodyLoader
            width: composite.width - 50
            sourceComponent: composite.body
        }
    }

    onClicked: {
        composite.expanded = !composite.expanded
    }
}