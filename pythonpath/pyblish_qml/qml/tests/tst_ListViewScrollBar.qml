import QtQuick 2.0;


Item {
    id: root

    width: 500
    height: 500

    ListView {
        id: listview

        anchors.fill: parent

        model: 20
        delegate: Rectangle {
            height: 50
            width: root.width
            color: modelData % 2 ? "steelblue" : "lightblue"
        }
    }

    ScrollBar {
        flickable: listview
    }
}