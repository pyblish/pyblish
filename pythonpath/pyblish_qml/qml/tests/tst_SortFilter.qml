import QtQuick 2.3
import QtQuick.Controls 1.3


Rectangle {
    width: 200
    height: 300
    color: "brown"

    TextField {
        id: edit

        placeholderText: "Filter.."

        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right

        anchors.margins: 10

        onTextChanged: qmodel.setFilterFixedString(text)
    }

    Rectangle {
        color: "white"
        radius: 2

        anchors.top: edit.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 10

        ListView {
            id: listView

            clip: true

            model: qmodel
            spacing: 10

            anchors.fill: parent
            anchors.margins: 5

            delegate: Text {
                text: name
            }
        }
    }

}
