import QtQuick 2.3
import Pyblish 0.1


BaseDelegate {

    height: 16 + 5

    body: Row {
        spacing: 10

        anchors.verticalCenter: parent.verticalCenter

        AwesomeIcon {
            name: "file"
        }

        Label {
            text: object.message
            style: "body2"
            anchors.verticalCenter: parent.verticalCenter
        }
    }
}