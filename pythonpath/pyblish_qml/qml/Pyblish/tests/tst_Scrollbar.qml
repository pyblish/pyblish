import QtQuick 2.0
import Pyblish 0.1

Item {
    id: root

    width: 500
    height: 500

    ListView {
        id: listview

        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        // anchors.margins: 10
        width: parent.width - 20

        model: 20

        delegate: Rectangle {
            height: 50
            width: parent.width
            color: modelData % 2 ? "steelblue" : "lightblue"
        }
    }

    Scrollbar {
        flickable: listview

        anchors.top: flickable.top
        anchors.bottom: flickable.bottom
        anchors.right: parent.right

        width: 20
    }
}