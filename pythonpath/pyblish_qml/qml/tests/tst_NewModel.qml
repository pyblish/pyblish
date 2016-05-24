import QtQuick 2.0


Rectangle {
    width: 300
    height: 300
    color: "brown"

    ListView {
        clip: true

        model: pyModel

        anchors.fill: parent
        anchors.margins: 5

        delegate: Text {
            text: kLabel
            color: kColor
        }
    }
}
