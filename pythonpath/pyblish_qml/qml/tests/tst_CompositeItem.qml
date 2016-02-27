import QtQuick 2.3

Item {
    id: composite

    property Component body

    Row {
        anchors.fill: parent

        Rectangle {
            color: "brown"
            width: 50
            height: parent.height
        }

        Loader {
            width: parent.width - 50
            height: parent.height
            sourceComponent: composite.body
        }
    }

    body: Rectangle {
        height: 60

        color: "steelblue"
    }
}